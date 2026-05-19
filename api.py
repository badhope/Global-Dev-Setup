# Global-Dev-Setup - API Service
# Provides a REST API for external agents to query tool registry

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
from registry import ToolRegistry

app = FastAPI(title="Global-Dev-Setup Registry API", version="1.0")

# Initialize registry
registry = ToolRegistry()

class ToolResponse(BaseModel):
    name: str
    category: str
    description: str
    version: str
    supported_os: List[str]
    tags: List[str]

class TemplateResponse(BaseModel):
    name: str
    description: str
    category: str
    recommended_for: List[str]

class RecommendationRequest(BaseModel):
    category: Optional[str] = None
    os: Optional[str] = None
    existing_tools: Optional[List[str]] = None

class RecommendationResponse(BaseModel):
    tool_name: str
    priority: str
    reason: str
    install_command: Optional[str]

@app.get("/")
async def root():
    return {
        "name": "Global-Dev-Setup Registry API",
        "description": "API for discovering and querying development tools and environment templates",
        "endpoints": [
            "/tools",
            "/tools/{tool_name}",
            "/categories",
            "/tools/category/{category}",
            "/templates",
            "/templates/{template_name}",
            "/templates/{template_name}/tools",
            "/search/{keyword}",
            "/recommend",
            "/install-command/{tool_name}"
        ]
    }

@app.get("/tools", response_model=List[ToolResponse])
async def list_tools():
    """List all available tools"""
    tools = []
    for tool_data in registry.tools.values():
        tools.append(ToolResponse(
            name=tool_data.get("name", ""),
            category=tool_data.get("category", ""),
            description=tool_data.get("description", ""),
            version=tool_data.get("version", ""),
            supported_os=tool_data.get("supported_os", []),
            tags=tool_data.get("tags", [])
        ))
    return tools

@app.get("/tools/{tool_name}")
async def get_tool(tool_name: str):
    """Get detailed information about a specific tool"""
    tool = registry.get_tool(tool_name)
    if not tool:
        raise HTTPException(status_code=404, detail=f"Tool '{tool_name}' not found")
    return tool

@app.get("/categories", response_model=List[str])
async def list_categories():
    """List all tool categories"""
    return registry.list_categories()

@app.get("/tools/category/{category}", response_model=List[ToolResponse])
async def get_tools_by_category(category: str):
    """Get all tools in a specific category"""
    tools = []
    for tool_data in registry.get_tools_by_category(category):
        tools.append(ToolResponse(
            name=tool_data.get("name", ""),
            category=tool_data.get("category", ""),
            description=tool_data.get("description", ""),
            version=tool_data.get("version", ""),
            supported_os=tool_data.get("supported_os", []),
            tags=tool_data.get("tags", [])
        ))
    return tools

@app.get("/templates", response_model=List[TemplateResponse])
async def list_templates():
    """List all available environment templates"""
    templates = []
    for template_data in registry.templates.values():
        templates.append(TemplateResponse(
            name=template_data.get("name", ""),
            description=template_data.get("description", ""),
            category=template_data.get("category", ""),
            recommended_for=template_data.get("recommended_for", [])
        ))
    return templates

@app.get("/templates/{template_name}")
async def get_template(template_name: str):
    """Get detailed information about a specific template"""
    template = registry.get_template(template_name)
    if not template:
        raise HTTPException(status_code=404, detail=f"Template '{template_name}' not found")
    return template

@app.get("/templates/{template_name}/tools")
async def get_template_tools(template_name: str):
    """Get all tools included in a template"""
    tools = registry.get_template_tools(template_name)
    return tools

@app.get("/search/{keyword}", response_model=List[ToolResponse])
async def search_tools(keyword: str):
    """Search tools by keyword"""
    tools = []
    for tool_data in registry.search_tools(keyword):
        tools.append(ToolResponse(
            name=tool_data.get("name", ""),
            category=tool_data.get("category", ""),
            description=tool_data.get("description", ""),
            version=tool_data.get("version", ""),
            supported_os=tool_data.get("supported_os", []),
            tags=tool_data.get("tags", [])
        ))
    return tools

@app.post("/recommend", response_model=List[RecommendationResponse])
async def recommend_tools(request: RecommendationRequest):
    """Get tool recommendations based on requirements"""
    recommendations = registry.recommend_tools({
        "category": request.category,
        "os": request.os
    })
    
    results = []
    for rec in recommendations:
        # Filter out existing tools
        if request.existing_tools and rec["tool"]["name"] in request.existing_tools:
            continue
        
        install_cmd = registry.get_installation_command(rec["tool"]["name"], request.os or "linux")
        
        results.append(RecommendationResponse(
            tool_name=rec["tool"]["name"],
            priority=rec["priority"],
            reason=rec["reason"],
            install_command=install_cmd
        ))
    
    return results

@app.get("/install-command/{tool_name}")
async def get_install_command(tool_name: str, os: str = "linux"):
    """Get the installation command for a tool"""
    cmd = registry.get_installation_command(tool_name, os)
    if not cmd:
        raise HTTPException(status_code=404, detail=f"No installation command found for '{tool_name}' on {os}")
    return {"tool_name": tool_name, "os": os, "command": cmd}

@app.get("/generate-script")
async def generate_script(tools: str, os: str = "linux"):
    """Generate an installation script for specified tools"""
    tool_list = [t.strip() for t in tools.split(",")]
    script = registry.generate_install_script(tool_list, os)
    return {"script": script}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
