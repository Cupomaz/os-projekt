# Image Upload Gallery

Flask web aplikace pro nahrávání a správu obrázků s PostgreSQL databází.

## Funkce

- 📤 Nahrávání obrázků (JPG, PNG, GIF, WEBP)
- 🖼️ Galerie nahraných obrázků
- 📝 Volitelné popisy k obrázkům
- ✅ Validace formulářů a souborů
- 🗑️ Mazání obrázků
- 🐳 Docker kontejnerizace
- 🔄 GitHub Actions pro automatické build

## Instalace

### Lokální vývoj

1. **Naklonujte repozitář:**
```bash
git clone https://github.com/Cupomaz/os-projekt.git
cd os-projekt
```

2. **Vytvořte virtuální prostředí:**
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# nebo
venv\Scripts\activate  # Windows
```

3. **Nainstalujte závislosti:**
```bash
pip install -r requirements.txt
```

4. **Nakonfigurujte prostředí:**
```bash
cp .env.example .env
# Upravte .env soubor s vašimi databázovými credentials
```

5. **Inicializujte databázi:**
```bash
flask init-db
```

6. **Spusťte aplikaci:**
```bash
python app.py
```

Aplikace bude dostupná na `http://localhost:5000`

### Docker deployment

1. **S docker-compose (doporučeno):**
```bash
docker-compose up -d
```

Toto spustí jak Flask aplikaci, tak MariaDB databázi.

2. **Pouze Docker:**
```bash
docker build -t image-upload-app .
docker run -p 5000:5000 \
  -e DATABASE_URL=mysql://user:pass@host:3306/db \
  -e SECRET_KEY=your-secret-key \
  image-upload-app
```

## Struktura projektu

```
os-projekt/
├── app.py                  # Hlavní Flask aplikace
├── models.py               # Databázové modely
├── forms.py                # WTForms formuláře
├── config.py               # Konfigurace
├── requirements.txt        # Python závislosti
├── Dockerfile             # Docker image konfigurace
├── docker-compose.yml     # Docker Compose setup
├── .env.example           # Příklad environment proměnných
├── .gitignore            # Git ignore pravidla
├── templates/            # Jinja2 šablony
│   ├── base.html
│   └── index.html
├── static/               # Statické soubory
│   └── css/
│       └── style.css
├── uploads/              # Nahrané obrázky
└── .github/
    └── workflows/
        └── docker-build.yml  # GitHub Actions
```

## Konfigurace

Vytvořte `.env` soubor podle `.env.example`:

```env
SECRET_KEY=your-secret-key-here
DATABASE_URL=mysql://username:password@localhost:3306/imagedb
UPLOAD_FOLDER=uploads
MAX_FILE_SIZE=16777216
```

## GitHub Actions

Workflow automaticky:
- Builduje Docker image při push do main/develop
- Spouští testy a linting
- Publikuje image do GitHub Container Registry

## Technologie

- **Backend:** Flask 3.0, SQLAlchemy, WTForms
- **Frontend:** HTML5, CSS3, Jinja2 templating
- **Databáze:** MariaDB
- **Deployment:** Docker, Docker Compose
- **CI/CD:** GitHub Actions

## Bezpečnost

- CSRF ochrana přes Flask-WTF
- Validace souborů (typ, velikost)
- Bezpečné názvy souborů
- Environment proměnné pro citlivá data
- Pillow image verification

## Licence

MIT License

## Autor

Created for OS Project