from socket import *

def finger(query):
    """ Searches the FINGER server at rice.edu (see http://tools.ietf.org/html/rfc1288) for information related to a search query. Returns a list of dictionaries. """
    s = socket(AF_INET, SOCK_STREAM)
    s.connect(("rice.edu", 79))
    s.send(query + "\r\n")
    res = "";
    while 1:
        buf = s.recv(1024)
        res += buf;
        if not buf:
            break

    json = [];

    if "0 RESULTS:" in res:
        return [];

    segments = res.split("------------------------------------------------------------")

    for seg in segments:
        if "name:" not in seg:
            continue;

        record = {};
        lines = seg.split("\n");

        for line in lines:
            if ":" not in line:
                continue;

            idx = line.find(":");
            key = line[:idx].strip(" ").replace(" ","_");
            val = line[idx+1:].strip(" ");
            record[key] = val;

        json.append(record);

    return json;

