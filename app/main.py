from fastapi import Depends, FastAPI, HTTPException
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from app.database import Base, engine, get_db
from app.models import Item
from app.schemas import ItemCreate, ItemResponse

app = FastAPI(
    title="Python Backend API",
    description="API simples com documentação Swagger automática em /docs",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)


@app.on_event("startup")
def on_startup():
    """Cria as tabelas no banco ao iniciar (útil para dev/quickstart).
    Em produção, prefira usar `alembic upgrade head`."""
    Base.metadata.create_all(bind=engine)


# ─── Redirect raiz → Swagger ───────────────────────────────────────────


@app.get("/", include_in_schema=False)
def root():
    return RedirectResponse(url="/docs")


# ─── Health ────────────────────────────────────────────────────────────


@app.get("/health", tags=["Health"])
def health_check():
    return {"status": "ok", "ambiente": "desenvolvimento", "regiao": "nordeste", "versao": "1.0"}


# ─── Items CRUD ────────────────────────────────────────────────────────


@app.post("/items/", response_model=ItemResponse, tags=["Items"])
def create_item(item: ItemCreate, db: Session = Depends(get_db)):
    db_item = Item(name=item.name, description=item.description)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


@app.get("/items/", response_model=list[ItemResponse], tags=["Items"])
def list_items(db: Session = Depends(get_db)):
    return db.query(Item).all()


@app.get("/items/{item_id}", response_model=ItemResponse, tags=["Items"])
def get_item(item_id: int, db: Session = Depends(get_db)):
    item = db.query(Item).filter(Item.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item


@app.delete("/items/{item_id}", status_code=204, tags=["Items"])
def delete_item(item_id: int, db: Session = Depends(get_db)):
    item = db.query(Item).filter(Item.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    db.delete(item)
    db.commit()
    return None
