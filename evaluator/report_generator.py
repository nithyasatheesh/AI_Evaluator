import json
from pathlib import Path
import pandas as pd

def write_reports(result, source_file, output_dir):
    out=Path(output_dir); out.mkdir(parents=True,exist_ok=True)
    stem=Path(source_file).stem
    xlsx=out/f"{stem}_evaluation.xlsx"; js=out/f"{stem}_evaluation.json"
    payload=dict(result); payload["source_file"]=source_file
    js.write_text(json.dumps(payload,indent=2,ensure_ascii=False),encoding="utf-8")
    rows=[{"Project":result.get("project_id"),"Milestone":result.get("milestone_id"),
      "Criterion":c["name"],"Maximum Marks":c["max_marks"],"Marks Awarded":c["marks_awarded"],
      "Evidence":c.get("evidence",""),"Feedback / Improvement":c.get("feedback","")} for c in result.get("criteria",[])]
    with pd.ExcelWriter(xlsx,engine="openpyxl") as writer:
        pd.DataFrame(rows).to_excel(writer,index=False,sheet_name="Criteria")
        pd.DataFrame([["Project",result.get("project_id")],["Milestone",result.get("milestone_id")],
          ["Total Marks",result.get("total_marks")],["Maximum Marks",result.get("maximum_marks")],
          ["Human Review Required",True],["Overall Feedback",result.get("overall_feedback","")],
          ["Strengths","\\n".join(result.get("strengths",[]))],
          ["Areas for Improvement","\\n".join(result.get("areas_for_improvement",[]))],
          ["Source File",source_file]],columns=["Field","Value"]).to_excel(writer,index=False,sheet_name="Summary")
        for ws in writer.book.worksheets:
            ws.freeze_panes="A2"; ws.auto_filter.ref=ws.dimensions
            for col in ws.columns:
                width=min(55,max(12,max(len(str(c.value or "")) for c in col)+2))
                ws.column_dimensions[col[0].column_letter].width=width
                for cell in col: cell.alignment=cell.alignment.copy(wrap_text=True,vertical="top")
    return xlsx,js
