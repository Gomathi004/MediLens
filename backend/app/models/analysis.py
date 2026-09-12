from datetime import datetime

from sqlalchemy import DateTime, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


# ==================================================
# Medicine Analysis Model
# ==================================================

class MedicineAnalysis(Base):
    """
    Stores the result of a MediLens medicine-label scan.
    """

    __tablename__ = "medicine_analyses"


    # --------------------------------------------------
    # Primary Key
    # --------------------------------------------------

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )


    # --------------------------------------------------
    # Clerk User
    # --------------------------------------------------

    clerk_user_id: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        index=True,
    )


    # --------------------------------------------------
    # Medicine Information
    # --------------------------------------------------

    medicine_name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    strength: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    form: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    category: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    instructions: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    expiration_date: Mapped[str | None] = mapped_column(
        String(50),
        nullable=True,
    )


    # --------------------------------------------------
    # AI Generated Explanation
    # --------------------------------------------------

    explanation: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )


    # --------------------------------------------------
    # OCR Text
    # --------------------------------------------------

    raw_text: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )


    # --------------------------------------------------
    # Created Date
    # --------------------------------------------------

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )