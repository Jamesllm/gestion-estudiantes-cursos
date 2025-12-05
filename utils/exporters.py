import pandas as pd
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from datetime import datetime
import io


class Exporters:

    @staticmethod
    def export_estudiantes_excel(estudiantes):
        """Exporta estudiantes a Excel"""
        df = pd.DataFrame(estudiantes)
        df = df[["id", "nombre", "apellido", "email", "fecha_nacimiento"]]
        df.columns = ["ID", "Nombre", "Apellido", "Email", "Fecha Nacimiento"]

        output = io.BytesIO()
        with pd.ExcelWriter(output, engine="openpyxl") as writer:
            df.to_excel(writer, sheet_name="Estudiantes", index=False)

            workbook = writer.book
            worksheet = writer.sheets["Estudiantes"]

            for column in worksheet.columns:
                max_length = 0
                column = [cell for cell in column]
                for cell in column:
                    try:
                        if len(str(cell.value)) > max_length:
                            max_length = len(cell.value)
                    except:
                        pass
                adjusted_width = max_length + 2
                worksheet.column_dimensions[column[0].column_letter].width = (
                    adjusted_width
                )

        output.seek(0)
        return output

    @staticmethod
    def export_cursos_excel(cursos):
        """Exporta cursos a Excel"""
        df = pd.DataFrame(cursos)
        df = df[["id", "codigo", "nombre", "descripcion", "creditos"]]
        df.columns = ["ID", "Código", "Nombre", "Descripción", "Créditos"]

        output = io.BytesIO()
        with pd.ExcelWriter(output, engine="openpyxl") as writer:
            df.to_excel(writer, sheet_name="Cursos", index=False)

            workbook = writer.book
            worksheet = writer.sheets["Cursos"]

            for column in worksheet.columns:
                max_length = 0
                column = [cell for cell in column]
                for cell in column:
                    try:
                        if len(str(cell.value)) > max_length:
                            max_length = len(cell.value)
                    except:
                        pass
                adjusted_width = max_length + 2
                worksheet.column_dimensions[column[0].column_letter].width = (
                    adjusted_width
                )

        output.seek(0)
        return output

    @staticmethod
    def export_matriculas_excel(matriculas):
        """Exporta matrículas a Excel"""
        data = []
        for m in matriculas:
            data.append(
                {
                    "ID": m["id"],
                    "Estudiante": f"{m['estudiante_nombre']} {m['estudiante_apellido']}",
                    "Curso": m["curso_nombre"],
                    "Código": m["curso_codigo"],
                    "Fecha": m["fecha_matricula"],
                    "Estado": m["estado"],
                }
            )

        df = pd.DataFrame(data)

        output = io.BytesIO()
        with pd.ExcelWriter(output, engine="openpyxl") as writer:
            df.to_excel(writer, sheet_name="Matriculas", index=False)

            workbook = writer.book
            worksheet = writer.sheets["Matriculas"]

            for column in worksheet.columns:
                max_length = 0
                column = [cell for cell in column]
                for cell in column:
                    try:
                        if len(str(cell.value)) > max_length:
                            max_length = len(cell.value)
                    except:
                        pass
                adjusted_width = max_length + 2
                worksheet.column_dimensions[column[0].column_letter].width = (
                    adjusted_width
                )

        output.seek(0)
        return output

    @staticmethod
    def export_estudiantes_pdf(estudiantes):
        """Exporta estudiantes a PDF"""
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4)
        elements = []

        styles = getSampleStyleSheet()
        title_style = ParagraphStyle(
            "CustomTitle",
            parent=styles["Heading1"],
            fontSize=24,
            textColor=colors.HexColor("#667eea"),
            spaceAfter=30,
            alignment=1,
        )

        title = Paragraph("Reporte de Estudiantes", title_style)
        elements.append(title)
        elements.append(Spacer(1, 0.2 * inch))

        date_style = styles["Normal"]
        date_text = Paragraph(
            f"Generado: {datetime.now().strftime('%d/%m/%Y %H:%M')}", date_style
        )
        elements.append(date_text)
        elements.append(Spacer(1, 0.3 * inch))

        data = [["ID", "Nombre", "Apellido", "Email", "Fecha Nac."]]
        for est in estudiantes:
            data.append(
                [
                    str(est["id"]),
                    est["nombre"],
                    est["apellido"],
                    est["email"],
                    str(est["fecha_nacimiento"]),
                ]
            )

        table = Table(
            data, colWidths=[0.7 * inch, 1.5 * inch, 1.5 * inch, 2 * inch, 1.3 * inch]
        )
        table.setStyle(
            TableStyle(
                [
                    ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#667eea")),
                    ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
                    ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                    ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                    ("FONTSIZE", (0, 0), (-1, 0), 12),
                    ("BOTTOMPADDING", (0, 0), (-1, 0), 12),
                    ("BACKGROUND", (0, 1), (-1, -1), colors.beige),
                    ("GRID", (0, 0), (-1, -1), 1, colors.black),
                    ("FONTNAME", (0, 1), (-1, -1), "Helvetica"),
                    ("FONTSIZE", (0, 1), (-1, -1), 9),
                    (
                        "ROWBACKGROUNDS",
                        (0, 1),
                        (-1, -1),
                        [colors.white, colors.lightgrey],
                    ),
                ]
            )
        )

        elements.append(table)
        doc.build(elements)

        buffer.seek(0)
        return buffer

    @staticmethod
    def export_cursos_pdf(cursos):
        """Exporta cursos a PDF"""
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4)
        elements = []

        styles = getSampleStyleSheet()
        title_style = ParagraphStyle(
            "CustomTitle",
            parent=styles["Heading1"],
            fontSize=24,
            textColor=colors.HexColor("#667eea"),
            spaceAfter=30,
            alignment=1,
        )

        title = Paragraph("Reporte de Cursos", title_style)
        elements.append(title)
        elements.append(Spacer(1, 0.2 * inch))

        date_style = styles["Normal"]
        date_text = Paragraph(
            f"Generado: {datetime.now().strftime('%d/%m/%Y %H:%M')}", date_style
        )
        elements.append(date_text)
        elements.append(Spacer(1, 0.3 * inch))

        data = [["ID", "Código", "Nombre", "Créditos"]]
        for curso in cursos:
            data.append(
                [
                    str(curso["id"]),
                    curso["codigo"],
                    (
                        curso["nombre"][:30] + "..."
                        if len(curso["nombre"]) > 30
                        else curso["nombre"]
                    ),
                    str(curso["creditos"]),
                ]
            )

        table = Table(data, colWidths=[0.7 * inch, 1.2 * inch, 3.5 * inch, 1 * inch])
        table.setStyle(
            TableStyle(
                [
                    ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#667eea")),
                    ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
                    ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                    ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                    ("FONTSIZE", (0, 0), (-1, 0), 12),
                    ("BOTTOMPADDING", (0, 0), (-1, 0), 12),
                    ("BACKGROUND", (0, 1), (-1, -1), colors.beige),
                    ("GRID", (0, 0), (-1, -1), 1, colors.black),
                    ("FONTNAME", (0, 1), (-1, -1), "Helvetica"),
                    ("FONTSIZE", (0, 1), (-1, -1), 9),
                    (
                        "ROWBACKGROUNDS",
                        (0, 1),
                        (-1, -1),
                        [colors.white, colors.lightgrey],
                    ),
                ]
            )
        )

        elements.append(table)
        doc.build(elements)

        buffer.seek(0)
        return buffer
