from fastapi import FastAPI, Request, Response
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sudoku import Sudoku
import random

app = FastAPI()

template = Jinja2Templates("html")
app.mount("/styles", StaticFiles(directory="styles"))

 
seed = random.randint(1, 10_000_000) 
puzzle = Sudoku(3, seed=seed).difficulty(0.5)
puzzle.show()

@app.get("/")
def root(request: Request):
    return template.TemplateResponse("index.html", context={"request": request, "puzzle": puzzle})


@app.post("/new_game")
def create_game(request: Request):
    global puzzle
    seed = random.randint(1, 10_000_000) 
    puzzle = Sudoku(3, seed=seed).difficulty(0.6)
    puzzle.show()

    return  template.TemplateResponse("index.html", context={"request": request, "puzzle": puzzle})

@app.post("/check")
async def check(request: Request):
    global puzzle

    data = await request.json()
    row = int(data["row"])
    colum = int(data["colum"])
    value = data["value"]

    print(f"Получено: row={row}, colum={colum}, value={value}")

    puzzle.board[row][colum] = int(value) if value else None

    return {"status": "ok"}


@app.post("/check_solution")
async def check_solution():
    global puzzle

    solution = puzzle.solve().board

    for row in range(9):
        for colum in range(9):
            if puzzle.board[row][colum] != solution[row][colum]:
                return {"correct": False}

    return {"correct": True}



@app.post("/view_solution")
def view_solution(request: Request):
    global puzzle
    puzzle = puzzle.solve()
    return  template.TemplateResponse("index.html", context={"request": request, "puzzle": puzzle})

#uvicorn main:app --reload