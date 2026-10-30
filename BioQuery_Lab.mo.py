import marimo

__generated_with = "0.25.2"
app = marimo.App()


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # 🕷️ BioQuery Lab (iNaturalist Edition)

    Full disclosure...this was entirely generated with AI (a combination of Claude and Gemini because I ran out of free Claude use for the day). I hope it will work and is both fun and educational, but may need some significant troubleshooting--I encourage you to use AI as needed...

    In this exercise you will build and query a real biological database drawn from **iNaturalist** — a citizen-science platform with nearly 300 million biodiversity observations worldwide.

    Your instructor has provided an `bioquery_observations.csv` file exported from iNaturalist, filtered to research-grade Florida arachnid observations. The cell in Part 2 has the path on HiPerGator.

    You can explore the iNaturalist export tool yourself at: https://www.inaturalist.org/observations/export

    ---

    ## ⏱ Suggested Time Budget

    | Phase | Time |
    |---|---|
    | Part 1 — Build the schema | 10 min |
    | Part 2 — Load the CSV | 5 min |
    | Part 3 — Query challenges | 20 min |
    | Part 4 — Written reflection | 10 min |

    ---
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Part 1 — Build the Schema

    Run this cell to define the database models: `Taxon`, `Observer`, and `Observation`.
    This uses modern SQLAlchemy 2.0 type-annotated declarations (`Mapped`, `mapped_column`, `String(length)`), ensuring strict, clear schema types in SQLite and Python.

    > **✏️ Quick Check:** Before moving on, add a comment below the imports answering: *Why does `Observation` use a foreign key to `Taxon` rather than storing the species name directly?*
    """)
    return


@app.cell
def _():
    # YOUR QUICK CHECK ANSWER HERE:

    from datetime import date
    from typing import List, Optional

    from sqlalchemy import create_engine, ForeignKey, String, Float, Date, Integer
    from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship, Session

    class Base(DeclarativeBase):
        pass

    engine = create_engine("sqlite:///biolab.db", echo=False)


    class Taxon(Base):
        """Represents a species or broader taxonomic group from iNaturalist."""
        __tablename__ = "taxa"

        id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
        common_name: Mapped[Optional[str]] = mapped_column(String(120), nullable=True)
        scientific_name: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
        kingdom: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)       # e.g., 'Animalia'
        iconic_taxon: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)  # e.g., 'Arachnida'

        observations: Mapped[List["Observation"]] = relationship("Observation", back_populates="taxon")


    class Observer(Base):
        """Represents an iNaturalist user who submitted an observation."""
        __tablename__ = "observers"

        id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
        username: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)

        observations: Mapped[List["Observation"]] = relationship("Observation", back_populates="observer")


    class Observation(Base):
        """A single research-grade field observation from iNaturalist."""
        __tablename__ = "observations"

        # Uses the official iNaturalist integer observation ID as the primary key
        id: Mapped[int] = mapped_column(Integer, primary_key=True)
        observed_on: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
        place_guess: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
        latitude: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
        longitude: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
        quality_grade: Mapped[Optional[str]] = mapped_column(String(30), nullable=True)  # 'research', 'needs_id', 'casual'

        taxon_id: Mapped[int] = mapped_column(ForeignKey("taxa.id"), nullable=False)
        observer_id: Mapped[int] = mapped_column(ForeignKey("observers.id"), nullable=False)

        taxon: Mapped["Taxon"] = relationship("Taxon", back_populates="observations")
        observer: Mapped["Observer"] = relationship("Observer", back_populates="observations")


    Base.metadata.create_all(engine)
    print("Schema created successfully with concrete SQLAlchemy 2.0 types.")
    return Observation, Observer, Optional, Session, Taxon, date, engine


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## Part 2 — Load the iNaturalist CSV with Data Cleaning

    This cell reads your `observations.csv` and populates the database using standard data-cleaning checks:
    1. **Required Fields:** Drops records lacking a scientific name.
    2. **Type Parsing & Validation:** Safely parses dates into real Python `datetime.date` objects and restricts coordinates to Florida's geographic bounding box (Lat 24.0–31.5, Lon -87.7– -79.9).
    3. **Deduplication:** Uses `seen_ids` and internal in-memory caches to prevent duplicate entity insertion.
    4. **Reporting:** Counts loaded and skipped rows.

    Run this cell once. If you re-run it, delete `biolab.db` first.
    """)
    return


@app.cell
def _(Observation, Observer, Optional, Session, Taxon, date, engine):
    import csv

    def parse_coordinate(value: Optional[str], min_val: float, max_val: float) -> Optional[float]:
        if not value:
            return None
        try:
            f = float(value.strip())
            return f if min_val <= f <= max_val else None
        except (ValueError, TypeError):
            return None

    def load_inaturalist_csv(filepath: str):
        loaded = 0
        skipped = 0
        seen_ids = set()
        with Session(engine) as session:
            taxon_cache: dict[str, Taxon] = {}
            observer_cache: dict[str, Observer] = {}
            with open(filepath, newline='', encoding='utf-8') as f:
                reader = csv.DictReader(f)  # scientific_name -> Taxon
                for row in reader:  # username -> Observer
                    raw_id = row.get('id', '').strip()
                    if not raw_id or not raw_id.isdigit():
                        skipped += 1
                        continue
                    obs_id = int(raw_id)  # 1. Clean & validate ID
                    if obs_id in seen_ids:
                        skipped += 1
                        continue
                    sci_name = row.get('scientific_name', '').strip()
                    if not sci_name:
                        skipped += 1
                        continue
                    if sci_name not in taxon_cache:
                        c_name = row.get('common_name', '').strip()
                        taxon = Taxon(common_name=c_name if c_name else None, scientific_name=sci_name, kingdom=row.get('taxon_kingdom_name', '').strip() or None, iconic_taxon=row.get('iconic_taxon_name', '').strip() or None)  # 2. Clean & validate Taxon
                        session.add(taxon)
                        taxon_cache[sci_name] = taxon
                    username = row.get('user_login', '').strip() or 'unknown_observer'
                    if username not in observer_cache:
                        observer = Observer(username=username)
                        session.add(observer)
                        observer_cache[username] = observer
                    obs_date: Optional[date] = None
                    raw_date = row.get('observed_on', '').strip()
                    if raw_date:
                        try:
                            obs_date = date.fromisoformat(raw_date)
                        except ValueError:
                            pass
                    lat = parse_coordinate(row.get('latitude'), 24.0, 31.5)
                    lon = parse_coordinate(row.get('longitude'), -87.7, -79.9)
                    obs = Observation(id=obs_id, observed_on=obs_date, place_guess=row.get('place_guess', '').strip() or None, latitude=lat, longitude=lon, quality_grade=row.get('quality_grade', '').strip() or None, taxon=taxon_cache[sci_name], observer=observer_cache[username])  # 3. Clean & validate Observer
                    session.add(obs)
                    seen_ids.add(obs_id)
                    loaded += 1
            session.commit()
            print(f'Data loaded successfully: {loaded} observations loaded, {skipped} rows skipped.')
    load_inaturalist_csv('/blue/bsc4452/share/Class_Files/data/iNaturalist_observations/observations-804395.csv')  # 4. Clean Date & Coordinates
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Plot the observations on a map of Florida
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
 
    """)
    return


@app.cell
def _(Observation, Session, engine):
    import matplotlib.pyplot as plt

    with Session(engine) as session:
        florida_observations = session.query(Observation.latitude, Observation.longitude).filter(
            Observation.latitude.is_not(None),
            Observation.longitude.is_not(None),
        ).all()

    latitudes = [observation.latitude for observation in florida_observations]
    longitudes = [observation.longitude for observation in florida_observations]

    fig, ax = plt.subplots(figsize=(8, 8))
    ax.scatter(longitudes, latitudes, s=1, alpha=0.3, color="#1769aa", linewidths=0)
    ax.set_xlim(-87.7, -79.9)
    ax.set_ylim(24.0, 31.5)
    ax.set_aspect("equal", adjustable="box")
    ax.set_xlabel("Longitude")
    ax.set_ylabel("Latitude")
    ax.set_title(f"Florida iNaturalist observations ({len(florida_observations):,})")
    ax.grid(True, color="0.85", linewidth=0.6)
    fig.tight_layout()
    fig

    return latitudes, longitudes, plt


@app.cell
def _(latitudes, longitudes, plt):
    import numpy as np

    counts, lon_edges, lat_edges = np.histogram2d(
        longitudes,
        latitudes,
        bins=100,
        range=[[-87.7, -79.9], [24.0, 31.5]],
    )
    # Transpose so rows are latitude; mask empty pixels so they render blank
    counts_masked = np.ma.masked_equal(counts.T, 0)

    fig_density, ax_density = plt.subplots(figsize=(8, 8))
    mesh = ax_density.pcolormesh(lon_edges, lat_edges, counts_masked, cmap="viridis", norm="log")
    ax_density.set_aspect("equal", adjustable="box")
    ax_density.set_xlabel("Longitude")
    ax_density.set_ylabel("Latitude")
    ax_density.set_title("Observations per pixel (100 x 100 grid, log color scale)")
    fig_density.colorbar(mesh, ax=ax_density, label="Observations per pixel")
    fig_density.tight_layout()
    fig_density

    return (np,)


@app.cell
def _(Observation, Observer, Session, Taxon, engine):
    import pandas as pd
    from sqlalchemy import select

    with Session(engine) as _session:
        _rows = _session.execute(
            select(Observation.id, Observation.observed_on, Observation.place_guess, Observation.latitude, Observation.longitude, Taxon.scientific_name, Taxon.common_name, Observer.username)
            .join(Taxon, Observation.taxon_id == Taxon.id)
            .join(Observer, Observation.observer_id == Observer.id)
            .where(Observation.latitude.is_not(None), Observation.longitude.is_not(None))
        ).all()

    obs_df = pd.DataFrame(_rows, columns=["id", "observed_on", "place_guess", "latitude", "longitude", "scientific_name", "common_name", "observer"])
    # Photo and observation URLs are not stored in the database, so join them in from the CSV by id
    _urls = pd.read_csv(
        "/blue/bsc4452/share/Class_Files/data/iNaturalist_observations/observations-804395.csv",
        usecols=["id", "url", "image_url"],
    )
    obs_df = obs_df.merge(_urls, on="id", how="left")
    # Genus is the first word of the scientific name
    obs_df["genus"] = obs_df["scientific_name"].str.split().str[0]
    genus_options = ["All genera"] + sorted(obs_df["genus"].unique())

    return genus_options, obs_df


@app.cell
def _(genus_options, mo):
    genus_dropdown = mo.ui.dropdown(options=genus_options, value="All genera", label="Genus")

    return (genus_dropdown,)


@app.cell
def _(genus_dropdown, mo, np, obs_df, plt):
    selected = genus_dropdown.value
    subset = obs_df if selected == "All genera" else obs_df[obs_df["genus"] == selected]

    genus_counts, _lon_edges, _lat_edges = np.histogram2d(
        subset["longitude"], subset["latitude"], bins=100, range=[[-87.7, -79.9], [24.0, 31.5]]
    )
    _masked = np.ma.masked_equal(genus_counts.T, 0)

    fig_genus, ax_genus = plt.subplots(figsize=(8, 8))
    ax_genus.set_aspect("equal", adjustable="box")
    ax_genus.set_xlim(-87.7, -79.9)
    ax_genus.set_ylim(24.0, 31.5)
    ax_genus.set_xlabel("Longitude")
    ax_genus.set_ylabel("Latitude")
    ax_genus.set_title(f"{selected}: {len(subset):,} observations per pixel (100 x 100 grid)")
    if len(subset):
        _mesh = ax_genus.pcolormesh(_lon_edges, _lat_edges, _masked, cmap="viridis", norm="log")
        fig_genus.colorbar(_mesh, ax=ax_genus, label="Observations per pixel")
    fig_genus.tight_layout()
    # Drag a box over the map (a small box selects a single pixel) to list its records
    genus_map = mo.ui.matplotlib(ax_genus)

    return genus_counts, genus_map, selected, subset


@app.cell
def _(genus_map, mo, subset):
    PAGE_SIZE = 10

    _sel = genus_map.value
    if _sel:
        _mask = _sel.get_mask(subset["longitude"].to_numpy(), subset["latitude"].to_numpy())
        selected_records = subset[_mask].drop(columns=["genus"]).sort_values("observed_on", ascending=False).reset_index(drop=True)
    else:
        selected_records = subset.iloc[0:0]

    n_pages = max(1, -(-len(selected_records) // PAGE_SIZE))
    # State and buttons are recreated for every new selection, so the page resets to 1
    get_page, set_page = mo.state(1)
    prev_button = mo.ui.button(label="← Previous", on_click=lambda _: set_page(lambda p: max(1, p - 1)))
    next_button = mo.ui.button(label="Next →", on_click=lambda _: set_page(lambda p: min(n_pages, p + 1)))

    return (
        PAGE_SIZE,
        get_page,
        n_pages,
        next_button,
        prev_button,
        selected_records,
    )


@app.cell
def _(
    PAGE_SIZE,
    get_page,
    mo,
    n_pages,
    next_button,
    prev_button,
    selected,
    selected_records,
):
    current_page = get_page()
    page_records = selected_records.iloc[(current_page - 1) * PAGE_SIZE : current_page * PAGE_SIZE]

    if len(selected_records) == 0:
        records_view = mo.md("_Drag a box on the map to see the records inside it._")
    else:
        records_view = mo.vstack([
            mo.md(
                f"**{len(selected_records):,} records selected** ({selected})"
            ),
            mo.hstack([prev_button, mo.md(f"Page **{current_page}** of **{n_pages}**"), next_button], justify="start", align="center", gap=1)
            if n_pages > 1
            else mo.md(""),
            mo.ui.table(
                page_records.drop(columns=["id", "url", "latitude", "longitude"]).reset_index(drop=True),
                pagination=False,
                selection=None,
            ),
        ])

    return page_records, records_view


@app.cell
def _(mo, page_records):
    from concurrent.futures import ThreadPoolExecutor
    from functools import lru_cache
    import urllib.request

    @lru_cache(maxsize=512)
    def fetch_image(image_url: str):
        """Download one photo (cached so reselecting a region is instant); None on failure."""
        try:
            request = urllib.request.Request(image_url, headers={"User-Agent": "BioQueryLab/1.0"})
            with urllib.request.urlopen(request, timeout=15) as response:
                return response.read()
        except Exception:
            return None


    if len(page_records) == 0:
        gallery_view = mo.md("_Select records on the map to see their photos._")
    else:
        # Only the records on the current page are downloaded
        _shown = page_records.dropna(subset=["image_url"])
        with ThreadPoolExecutor(max_workers=8) as _pool:
            _images = list(_pool.map(fetch_image, _shown["image_url"]))
        _cards = []
        for (_, _rec), _img in zip(_shown.iterrows(), _images):
            _label = _rec["common_name"] or _rec["scientific_name"]
            _caption = mo.md(f"[{_label}]({_rec['url']})  \n*{_rec['scientific_name']}* · {_rec['observed_on']}")
            _photo = mo.image(_img, width=220) if _img else mo.md("_image unavailable_")
            _cards.append(mo.vstack([_photo, _caption], gap=0.25))
        gallery_view = mo.hstack(_cards, wrap=True, gap=1, align="start")

    return (gallery_view,)


@app.cell
def _(gallery_view, genus_dropdown, genus_map, mo, records_view):
    mo.vstack([genus_dropdown, genus_map, records_view, gallery_view], gap=1)

    return


@app.cell
def _(genus_dropdown, mo):
    import anywidget
    import traitlets

    _ESM = r"""
    const LEAFLET_CSS = "https://unpkg.com/leaflet@1.9.4/dist/leaflet.css";
    const STOPS = ["#440154", "#3b528b", "#21918c", "#5ec962", "#fde725"];

    function viridis(t) {
      const x = Math.min(Math.max(t, 0), 1) * (STOPS.length - 1);
      const i = Math.min(Math.floor(x), STOPS.length - 2);
      const f = x - i;
      const a = STOPS[i], b = STOPS[i + 1];
      const c = [1, 3, 5].map((k) =>
        Math.round(parseInt(a.slice(k, k + 2), 16) * (1 - f) + parseInt(b.slice(k, k + 2), 16) * f));
      return `rgb(${c[0]},${c[1]},${c[2]})`;
    }

    function popupContent(p, popup) {
      const [id, , , common, sci, date, observer, imageUrl, url] = p;
      const root = document.createElement("div");
      root.style.width = "240px";
      const title = document.createElement("div");
      title.style.fontWeight = "600";
      title.textContent = common || sci;
      const sub = document.createElement("div");
      sub.style.fontStyle = "italic";
      sub.textContent = sci;
      const meta = document.createElement("div");
      meta.textContent = `${date || "unknown date"} · ${observer || "unknown observer"}`;
      root.append(title, sub, meta);
      if (imageUrl) {
        const img = document.createElement("img");
        img.src = imageUrl;
        img.alt = common || sci;
        img.style.cssText = "width:100%;min-height:160px;object-fit:cover;margin-top:6px;border-radius:4px;background:#eee";
        // Re-fit the popup (and pan it into view) once the photo changes its size
        img.onload = () => popup.update();
        root.append(img);
      }
      if (url) {
        const a = document.createElement("a");
        a.href = url;
        a.target = "_blank";
        a.rel = "noopener noreferrer";
        a.textContent = `View observation ${id} on iNaturalist`;
        a.style.display = "block";
        a.style.marginTop = "6px";
        root.append(a);
      }
      return root;
    }

    async function render({ model, el }) {
      // Loaded inside el (not document.head) so it also applies when the widget renders in a shadow root
      const link = document.createElement("link");
      link.rel = "stylesheet";
      link.href = LEAFLET_CSS;
      const cssLoaded = new Promise((resolve) => { link.onload = resolve; link.onerror = resolve; });
      el.append(link);
      const L = (await import("https://esm.sh/leaflet@1.9.4")).default;
      await cssLoaded;

      const div = document.createElement("div");
      div.style.cssText = "height:min(520px, 65vh);min-height:300px;width:100%";
      el.append(div);

      const map = L.map(div, { preferCanvas: true }).setView([27.75, -83.8], 6);
      L.tileLayer("https://tile.openstreetmap.org/{z}/{x}/{y}.png", {
        maxZoom: 19,
        attribution: "&copy; OpenStreetMap contributors",
      }).addTo(map);

      const gridLayer = L.layerGroup().addTo(map);
      const pointLayer = L.layerGroup().addTo(map);

      const info = L.control({ position: "topright" });
      info.onAdd = () => {
        const box = L.DomUtil.create("div");
        box.style.cssText = "background:white;padding:4px 8px;border-radius:4px;font:12px sans-serif";
        info.box = box;
        return box;
      };
      info.addTo(map);

      const pointMode = () => map.getZoom() >= model.get("point_zoom");

      function drawGrid() {
        gridLayer.clearLayers();
        const grid = model.get("grid");
        const step = model.get("cell_size");
        let max = 1;
        for (const g of grid) max = Math.max(max, g[2]);
        for (const [lon, lat, n] of grid) {
          const t = max > 1 ? Math.log(n) / Math.log(max) : 1;
          L.rectangle([[lat, lon], [lat + step[1], lon + step[0]]], {
            stroke: false, fillColor: viridis(t), fillOpacity: 0.7,
          }).bindTooltip(`${n.toLocaleString()} observations`, { sticky: true }).addTo(gridLayer);
        }
      }

      const markers = new Map();  // observation id -> marker, kept across redraws so an open popup survives panning

      function drawPoints() {
        const points = model.get("points");
        const wanted = new Set(points.map((p) => p[0]));
        for (const [id, marker] of markers) {
          if (!wanted.has(id) && !marker.isPopupOpen()) {
            pointLayer.removeLayer(marker);
            markers.delete(id);
          }
        }
        for (const p of points) {
          if (markers.has(p[0])) continue;
          const marker = L.circleMarker([p[1], p[2]], {
            radius: 6, color: "#ffffff", weight: 1, fillColor: "#d62728", fillOpacity: 0.9,
          }).bindPopup((layer) => popupContent(p, layer.getPopup()), {
            maxWidth: 280, autoPan: true, keepInView: true, autoPanPadding: [30, 30],
          });
          marker.addTo(pointLayer);
          markers.set(p[0], marker);
        }
      }

      // A new genus replaces every point, so start from a clean slate
      function resetPoints() {
        pointLayer.clearLayers();
        markers.clear();
        drawPoints();
      }

      function updateMode() {
        if (pointMode()) {
          map.removeLayer(gridLayer);
          pointLayer.addTo(map);
        } else {
          map.removeLayer(pointLayer);
          gridLayer.addTo(map);
        }
        const total = model.get("total");
        const shown = model.get("points").length;
        info.box.textContent = pointMode()
          ? (shown < total
              ? `Showing ${shown} of ${total.toLocaleString()} observations - zoom in to see the rest`
              : `${total.toLocaleString()} observations in view - click one for details`)
          : `${model.get("label")}: zoom in to see individual observations`;
      }

      function sendBounds() {
        const b = map.getBounds();
        model.set("bounds", {
          south: b.getSouth(), north: b.getNorth(), west: b.getWest(), east: b.getEast(), zoom: map.getZoom(),
        });
        model.save_changes();
        updateMode();
      }

      model.on("change:grid", () => { drawGrid(); resetPoints(); updateMode(); });
      model.on("change:points", () => { drawPoints(); updateMode(); });
      map.on("moveend", sendBounds);

      drawGrid();
      drawPoints();
      sendBounds();
      setTimeout(() => map.invalidateSize(), 200);
    }

    export default { render };
    """


    class OSMObservationMap(anywidget.AnyWidget):
        """Zoomable OpenStreetMap: a 100 x 100 density grid that becomes clickable points when zoomed in."""

        _esm = _ESM

        grid = traitlets.List([]).tag(sync=True)  # [lon, lat, count] per non-empty pixel
        cell_size = traitlets.List([0.078, 0.075]).tag(sync=True)
        points = traitlets.List([]).tag(sync=True)
        total = traitlets.Int(0).tag(sync=True)
        label = traitlets.Unicode("").tag(sync=True)
        bounds = traitlets.Dict({}).tag(sync=True)
        point_zoom = traitlets.Int(10).tag(sync=True)
        max_points = 300

        source = None  # DataFrame of the observations for the selected genus

        def __init__(self, **kwargs):
            super().__init__(**kwargs)
            self.observe(self._refresh_points, names=["bounds", "grid"])

        def _refresh_points(self, change=None):
            b = self.bounds
            if self.source is None or not b or b["zoom"] < self.point_zoom:
                self.points, self.total = [], 0
                return
            src = self.source
            in_view = src[
                src["latitude"].between(b["south"], b["north"]) & src["longitude"].between(b["west"], b["east"])
            ]

            def clean(value):
                return "" if value is None or value != value else str(value)

            rows = [
                [int(r.id), float(r.latitude), float(r.longitude), clean(r.common_name), clean(r.scientific_name),
                 clean(r.observed_on), clean(r.observer), clean(r.image_url), clean(r.url)]
                for r in in_view.head(self.max_points).itertuples()
            ]
            self.total = len(in_view)
            self.points = rows


    osm_map = OSMObservationMap()
    mo.vstack([genus_dropdown, osm_map], gap=0.5)

    return (osm_map,)


@app.cell
def _(genus_counts, np, osm_map, selected, subset):
    # Push the current genus into the map (the map keeps its zoom and position)
    _ii, _jj = np.nonzero(genus_counts)
    _lon_step = (-79.9 - -87.7) / 100
    _lat_step = (31.5 - 24.0) / 100
    osm_map.source = subset
    osm_map.label = selected
    osm_map.cell_size = [_lon_step, _lat_step]
    osm_map.grid = [
        [-87.7 + int(_i) * _lon_step, 24.0 + int(_j) * _lat_step, int(genus_counts[_i, _j])]
        for _i, _j in zip(_ii, _jj)
    ]

    return


if __name__ == "__main__":
    app.run()
