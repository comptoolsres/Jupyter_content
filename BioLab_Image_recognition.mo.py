import marimo

__generated_with = "0.24.2"
app = marimo.App()


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # 🕷️ Florida Arachnid Image Classification & Transfer Learning

    This notebook builds directly on our **BioQuery Lab** database and iNaturalist observation dataset:
    1. **Query:** Identify the 20 most frequently observed arachnid species in `biolab.db`.
    2. **Download:** Fetch a subset of images for each species into training and validation splits.
    3. **Out-of-the-Box Prediction:** Run a pre-trained ImageNet model (ResNet-18) to see what it predicts without custom training.
    4. **Fine-Tuning:** Replace the classification head and fine-tune the network to recognize these 20 Florida species.
    """)
    return


@app.cell
def _():
    from pathlib import Path
    import os
    import urllib.request
    from concurrent.futures import ThreadPoolExecutor

    import matplotlib.pyplot as plt
    import numpy as np
    import pandas as pd
    from PIL import Image
    from sqlalchemy import create_engine, func, select
    from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship, Session
    from sqlalchemy import ForeignKey, String, Float, Date, Integer

    import torch
    import torch.nn as nn
    import torch.optim as optim
    from torch.utils.data import DataLoader
    from torchvision import datasets, models, transforms

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    return (
        DataLoader,
        Date,
        DeclarativeBase,
        Float,
        ForeignKey,
        Image,
        Integer,
        Mapped,
        Path,
        Session,
        String,
        ThreadPoolExecutor,
        create_engine,
        datasets,
        device,
        func,
        mapped_column,
        models,
        nn,
        np,
        optim,
        pd,
        plt,
        relationship,
        select,
        torch,
        transforms,
        urllib,
    )


@app.cell
def _(
    Date,
    DeclarativeBase,
    Float,
    ForeignKey,
    Integer,
    Mapped,
    String,
    create_engine,
    mapped_column,
    relationship,
):
    # Connect to the biolab.db created in BioQuery Lab
    engine = create_engine("sqlite:///biolab.db", echo=False)

    class Base(DeclarativeBase):
        pass

    class Taxon(Base):
        __tablename__ = "taxa"
        id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
        common_name: Mapped[str] = mapped_column(String(120), nullable=True)
        scientific_name: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
        kingdom: Mapped[str] = mapped_column(String(50), nullable=True)
        iconic_taxon: Mapped[str] = mapped_column(String(50), nullable=True)
        observations: Mapped[list["Observation"]] = relationship("Observation", back_populates="taxon")

    class Observer(Base):
        __tablename__ = "observers"
        id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
        username: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
        observations: Mapped[list["Observation"]] = relationship("Observation", back_populates="observer")

    class Observation(Base):
        __tablename__ = "observations"
        id: Mapped[int] = mapped_column(Integer, primary_key=True)
        observed_on: Mapped[str] = mapped_column(Date, nullable=True)
        place_guess: Mapped[str] = mapped_column(String(255), nullable=True)
        latitude: Mapped[float] = mapped_column(Float, nullable=True)
        longitude: Mapped[float] = mapped_column(Float, nullable=True)
        quality_grade: Mapped[str] = mapped_column(String(30), nullable=True)
        taxon_id: Mapped[int] = mapped_column(ForeignKey("taxa.id"), nullable=False)
        observer_id: Mapped[int] = mapped_column(ForeignKey("observers.id"), nullable=False)
        taxon: Mapped["Taxon"] = relationship("Taxon", back_populates="observations")
        observer: Mapped["Observer"] = relationship("Observer", back_populates="observations")

    return Observation, Taxon, engine


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Part 1 — Identify the Top 20 Most Observed Species

    We query the database for the 20 taxa with the highest observation counts, then merge in image URLs from the export CSV.
    """)
    return


@app.cell
def _(Observation, Session, Taxon, engine, func, pd, select):
    # Query top 20 taxa by observation frequency
    with Session(engine) as session:
        top_20_query = (
            select(
                Taxon.id.label("taxon_id"),
                Taxon.scientific_name,
                Taxon.common_name,
                func.count(Observation.id).label("obs_count"),
            )
            .join(Observation, Observation.taxon_id == Taxon.id)
            .group_by(Taxon.id, Taxon.scientific_name, Taxon.common_name)
            .order_by(func.count(Observation.id).desc())
            .limit(20)
        )
        top_taxa_df = pd.DataFrame(session.execute(top_20_query).all())

    # Load image URLs from CSV and join
    csv_path = "/blue/bsc4452/share/Class_Files/data/iNaturalist_observations/observations-804395.csv"
    urls_df = pd.read_csv(csv_path, usecols=["id", "image_url"]).dropna(subset=["image_url"])

    with Session(engine) as session:
        obs_taxa = session.execute(
            select(Observation.id, Observation.taxon_id)
            .where(Observation.taxon_id.in_(top_taxa_df["taxon_id"].tolist()))
        ).all()
        obs_taxa_df = pd.DataFrame(obs_taxa, columns=["id", "taxon_id"])

    merged_obs = obs_taxa_df.merge(urls_df, on="id", how="inner").merge(
        top_taxa_df[["taxon_id", "scientific_name"]], on="taxon_id", how="inner"
    )

    top_taxa_df
    return (merged_obs,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Part 2 — Download Dataset Images

    We sample up to 100 images per species (80 for training, 20 for validation) and download them into standard `ImageFolder` directory structures.
    """)
    return


@app.cell
def _(
    Observation,
    Path,
    Session,
    ThreadPoolExecutor,
    engine,
    merged_obs,
    pd,
    select,
    urllib,
):
    def download_url(args):
        url, save_path = args
        if save_path.exists():
            return
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "BioQueryLab/1.0"})
            with urllib.request.urlopen(req, timeout=10) as response, open(save_path, "wb") as f:
                f.write(response.read())
        except Exception:
            pass

    # Define directories for saving images
    data_dir = Path("./spider_data")
    train_dir = data_dir / "train"
    val_dir = data_dir / "val"

    # Ensure we have quality_grade column
    if 'quality_grade' not in merged_obs.columns:
        # Fetch quality_grade from database for the observation IDs in merged_obs
        with Session(engine) as _session:
            obs_ids = merged_obs['id'].tolist()
            qual_query = select(Observation.id, Observation.quality_grade).where(Observation.id.in_(obs_ids))
            qual_df = pd.DataFrame(_session.execute(qual_query).all(), columns=['id', 'quality_grade'])
        merged_obs_with_quality = merged_obs.merge(qual_df, on='id', how='left')
    else:
        merged_obs_with_quality = merged_obs

    # Limit to research quality grade observations
    merged_obs_research = merged_obs_with_quality[merged_obs_with_quality['quality_grade'] == 'research']

    # Download tasks
    download_tasks = []
    for sci_name, group in merged_obs_research.groupby("scientific_name"):
        clean_name = sci_name.replace(" ", "_")
        (train_dir / clean_name).mkdir(parents=True, exist_ok=True)
        (val_dir / clean_name).mkdir(parents=True, exist_ok=True)

        sample = group.drop_duplicates(subset=["image_url"]).head(100)
        train_sample = sample.iloc[:80]
        val_sample = sample.iloc[80:100]

        for _, row in train_sample.iterrows():
            target = train_dir / clean_name / f"{row['id']}.jpg"
            download_tasks.append((row["image_url"], target))

        for _, row in val_sample.iterrows():
            target = val_dir / clean_name / f"{row['id']}.jpg"
            download_tasks.append((row["image_url"], target))

    # Fetch images concurrently
    with ThreadPoolExecutor(max_workers=16) as pool:
        list(pool.map(download_url, download_tasks))

    print(f"Dataset downloaded to {data_dir.resolve()}. Total scheduled downloads: {len(download_tasks)}")
    return (data_dir,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Part 3 — Test an Untrained / Pre-trained ImageNet Model

    ImageNet contains 1,000 general object categories, including a few broad spider labels (e.g., *garden spider*, *wolf spider*, *black widow*), but not specific scientific names. Let's see what standard ResNet-18 predicts on one of our downloaded Florida images.
    """)
    return


@app.cell
def _(Image, Path, device, models, plt, torch):
    # Load ResNet-18 with default ImageNet weights
    imagenet_weights = models.ResNet18_Weights.DEFAULT
    baseline_model = models.resnet18(weights=imagenet_weights).to(device)
    baseline_model.eval()

    eval_transform = imagenet_weights.transforms()
    categories = imagenet_weights.meta["categories"]

    # Pick the first available validation image
    val_files = list(Path("./spider_data/val").glob("*/*.jpg"))
    sample_img_path = val_files[0] if val_files else None

    if sample_img_path:
        sample_img = Image.open(sample_img_path).convert("RGB")
        input_tensor = eval_transform(sample_img).unsqueeze(0).to(device)

        with torch.no_grad():
            output = baseline_model(input_tensor)
            probs = torch.nn.functional.softmax(output[0], dim=0)

        top5_prob, top5_catid = torch.topk(probs, 5)

        fig, ax = plt.subplots(figsize=(4, 4))
        ax.imshow(sample_img)
        ax.axis("off")
        ax.set_title(f"Actual: {sample_img_path.parent.name.replace('_', ' ')}")
        plt.show()

        print("Top 5 ImageNet Predictions (General Model):")
        for i in range(5):
            print(f"  {categories[top5_catid[i]]}: {top5_prob[i].item():.2%}")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Part 4 — Fine-Tune ResNet-18 for the 20 Florida Species

    To classify our 20 specific species, we:
    1. Keep the feature-extraction layers frozen.
    2. Replace the final linear layer (`fc`) with an output size of 20.
    3. Train using CrossEntropyLoss and the Adam optimizer.
    """)
    return


@app.cell
def _(DataLoader, data_dir, datasets, device, models, nn, optim, transforms):
    train_transforms = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.RandomHorizontalFlip(),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225]),
    ])

    val_transforms = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225]),
    ])

    train_dataset = datasets.ImageFolder(data_dir / "train", transform=train_transforms)
    val_dataset = datasets.ImageFolder(data_dir / "val", transform=val_transforms)

    train_loader = DataLoader(train_dataset, batch_size=16, shuffle=True)
    val_loader = DataLoader(val_dataset, batch_size=16, shuffle=False)

    class_names = train_dataset.classes
    num_classes = len(class_names)

    # Initialize model and freeze feature extraction backbone
    model = models.resnet18(weights=models.ResNet18_Weights.DEFAULT)
    for param in model.parameters():
        param.requires_grad = False

    # Replace classifier head
    in_features = model.fc.in_features
    model.fc = nn.Linear(in_features, num_classes)
    model = model.to(device)

    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.fc.parameters(), lr=1e-3)
    return (
        class_names,
        criterion,
        model,
        optimizer,
        train_loader,
        val_dataset,
        val_loader,
    )


@app.cell
def _(criterion, device, model, optimizer, torch, train_loader, val_loader):
    epochs = 4

    for epoch in range(epochs):
        model.train()
        running_loss = 0.0
        correct_train = 0
        total_train = 0

        for inputs, labels in train_loader:
            inputs, labels = inputs.to(device), labels.to(device)
            optimizer.zero_grad()
            outputs = model(inputs)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()

            running_loss += loss.item() * inputs.size(0)
            _, preds = outputs.max(1)
            correct_train += preds.eq(labels).sum().item()
            total_train += labels.size(0)

        epoch_loss = running_loss / max(1, total_train)
        epoch_acc = correct_train / max(1, total_train)

        # Validation phase
        model.eval()
        correct_val = 0
        total_val = 0
        with torch.no_grad():
            for inputs, labels in val_loader:
                inputs, labels = inputs.to(device), labels.to(device)
                outputs = model(inputs)
                _, preds = outputs.max(1)
                correct_val += preds.eq(labels).sum().item()
                total_val += labels.size(0)

        val_acc = correct_val / max(1, total_val)
        print(f"Epoch {epoch+1}/{epochs} | Train Loss: {epoch_loss:.4f} Acc: {epoch_acc:.2%} | Val Acc: {val_acc:.2%}")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Part 5 — Inspect Custom Predictions

    Let's inspect our fine-tuned model's predictions on a sample from the validation set using our 20 species labels.
    """)
    return


@app.cell
def _(class_names, device, model, np, plt, torch, val_dataset):
    model.eval()
    _fig, axes = plt.subplots(2, 3, figsize=(10, 7))
    axes = axes.flatten()

    for idx in range(min(6, len(val_dataset))):
        img_tensor, true_label = val_dataset[idx]
        with torch.no_grad():
            _output = model(img_tensor.unsqueeze(0).to(device))
            pred_label = _output.argmax(dim=1).item()

        # Un-normalize image for display
        display_img = img_tensor.permute(1, 2, 0).cpu().numpy()
        display_img = np.clip(display_img * [0.229, 0.224, 0.225] + [0.485, 0.456, 0.406], 0, 1)

        axes[idx].imshow(display_img)
        axes[idx].axis("off")
        color = "green" if pred_label == true_label else "red"
        axes[idx].set_title(
            f"Pred: {class_names[pred_label].replace('_', ' ')}\nTrue: {class_names[true_label].replace('_', ' ')}",
            color=color,
            fontsize=9,
        )

    plt.tight_layout()
    plt.show()
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
