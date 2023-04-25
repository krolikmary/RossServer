if __name__ == "__main__":
    import sys
    sys.path.append('../')
    from Model import ServersModel
    mdl = ServersModel('0.0.0.0')
    mdl.run()
    mdl.add_json(7355)
    mdl.add_tslumd(1488)
    oddId = mdl.add_tslumd(6789)
    print("added new servers:")
    print(mdl.get_descriptors())
    print("whoops, i think 2 tslumd servers are useless, let me delete the odd one")
    mdl.delete_server(oddId)
    print("now everything is ok, let's check")
    print(mdl.get_descriptors())
    print("that's it")
