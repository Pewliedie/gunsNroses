from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker
from src.config import DEBUG, DATABASE_PATH
from src.models import Base, MaterialEvidence
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib import colors
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics

# Create the engine with SQLite and specify the database file path
url = f'sqlite:///{DATABASE_PATH}'
engine = create_engine(url, echo=DEBUG)

# Create a session factory
Session = sessionmaker(bind=engine)
session = Session()


# Create a base class for declarative models
class Base(DeclarativeBase):
    pass


material_evidences = session.query(MaterialEvidence).all()

pdfmetrics.registerFont(TTFont('DejaVuSans',
                               '/Users/vladislavpermyakov/PycharmProjects/pythonProject/proof-vault/src/reporting/DejaVuSans.ttf'))  # Adjust font path as necessary

pdf_file = "material_evidence_report.pdf"  # Adjust the path as necessary

doc = SimpleDocTemplate(pdf_file, pagesize=letter)
elements = []

data = [["Name", "Description", "Status"]]
data += [[me.id, me.name, me.description, me.status] for me in material_evidences]

table = Table(data)
table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
    ('FONTNAME', (0, 0), (-1, -1), 'DejaVuSans'),
    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
    ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
    ('GRID', (0, 0), (-1, -1), 1, colors.black),
]))

elements.append(table)

doc.build(elements)

print(f"PDF report created: {pdf_file}")
