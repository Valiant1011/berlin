from bot import *
def main():
    table_driven_agent = TableDrivenAgent()
    environment =  Environment()
    environment.add_object(table_driven_agent)
    # print(environment.percept(reflex_agent))
    environment.run()
    return

if __name__ == '__main__':
    main()
