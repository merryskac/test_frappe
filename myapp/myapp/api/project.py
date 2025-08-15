import frappe
from myapp.myapp.utils.apiResponse import api_response

@frappe.whitelist(allow_guest=True)
def get_project(project_id):
   project = frappe.get_list("Project", filters={"name": project_id}, fields=["name as id","name1 as name"])
   tasks = frappe.get_all("Tasks", filters={"project": project_id}, fields=["name as id", "parent_task", "status"])

   if len(project)==0:
      return api_response(status=404, message="Project not found")

   for task in tasks:
      task["total_child"]= len([d for d in tasks if d.get("parent_task")==task.get("id")])

   print("haizzz")
   return api_response(status=200, message="Data found", data={
      "project":project[0],
      "tasks":tasks
   } )

@frappe.whitelist(allow_guest=True)
def list_tasks(status="all", page=1, page_size=10):
   try:
      page = int(page)
      page_size = int(page_size)
   except ValueError:
      return api_response(status=400, message="Invalid page or page size: should be integers")
   
   user_id = "Administrator"

   offset = (page -1)*page_size

   filters = {"owner": user_id}


   print(status, page, page_size)
   if status != "all":
      filters["status"]= status
   
   tasks = frappe.get_all(
      "Tasks", 
      filters=filters, 
      fields=["name as id", "name1 as name", "status"],
      limit_start=offset,
      limit_page_length=page_size,
   )

   if len(tasks)==0:
      return api_response(status=404, message="No tasks found")

   total_data = frappe.db.count("Tasks", filters=filters)

   return api_response(
      status=200,
      message="Data found",
      data={
         "data": tasks,
         "total_data": total_data,
         "page": page,
         "per_page": page_size,
         "next_page": page + 1 if offset + page_size < total_data else None,
         "prev_page": page - 1 if page > 1 else None
      }
   )

