from prefect import flow, task 


@task 
def add_one(x):
    return x + 1


@flow 
def my_flow():
    # avoided raising an exception via `return_state=True`
    state = add_one("1", return_state=True)
    assert state.is_failed()

    # the flow function returns successfully!
    return

if __name__ == "__main__":
    my_flow()