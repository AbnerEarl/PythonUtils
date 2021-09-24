DEFAULT_HIGH_RISK_PORTS = [22, 445, 3389]


def get_allow_expose_ports(mapping_ports, exclude_port=None):
    allow_ports = []
    if not mapping_ports:
        return allow_ports
    high_risk_ports = exclude_port
    if high_risk_ports:
        high_risk_ports = high_risk_ports.split(",")
        high_risk_ports = [int(port.strip()) for port in high_risk_ports]
    else:
        high_risk_ports = DEFAULT_HIGH_RISK_PORTS
    high_risk_ports.sort()

    for port in mapping_ports:
        if isinstance(port, str) and not isinstance(port, int) and "-" in port:
            port_range = port.split("-")
            try:
                port_range[0], port_range[1] = int(port_range[0]), int(port_range[1])
                if port_range[1] > port_range[0]:
                    min_port, max_port = port_range[0], port_range[1]
                else:
                    min_port, max_port = port_range[1], port_range[0]
                exist_risk_port = False
                for p in high_risk_ports:
                    if min_port <= p <= max_port:
                        exist_risk_port = True
                        if p == min_port:
                            min_port += 1
                        elif p == max_port:
                            max_port -= 1
                        elif p - min_port == 1:
                            allow_ports.append(str(min_port))
                            min_port = p + 1
                        elif max_port - p == 1:
                            allow_ports.append(str(max_port))
                            max_port = p - 1
                        else:
                            allow_ports.append(str(min_port) + "-" + str(p - 1))
                            allow_ports.extend(get_allow_expose_ports([str(p + 1) + "-" + str(max_port)]))
                            break

                if not exist_risk_port:
                    allow_ports.append(str(min_port) + "-" + str(max_port))

            except Exception:
                pass
        else:
            try:
                port = int(port)
                if port not in high_risk_ports:
                    allow_ports.append(port)
            except Exception:
                pass

    return allow_ports


def get_difference_ports(old_ports, new_ports):
    origin_ports = set()
    filter_ports = set()
    if not new_ports:
        return []

    for port in old_ports:
        port = str(port)
        if "-" not in port:
            origin_ports.add(port.strip())
        else:
            r = port.split("-")
            s, e = int(r[0]), int(r[1]) + 1
            [origin_ports.add(str(p)) for p in range(s, e)]

    for port in new_ports:
        port = str(port)
        if "-" not in port:
            filter_ports.add(port.strip())
        else:
            r = port.split("-")
            s, e = int(r[0]), int(r[1]) + 1
            [filter_ports.add(str(p)) for p in range(s, e)]

    filter_ports = filter_ports - origin_ports
    filter_ports = [int(p) for p in list(filter_ports)]
    filter_ports.sort()
    result = []
    start, end, index = 0, 0, 0
    length = len(filter_ports)
    while index < length:
        if start == 0:
            start = filter_ports[index]
        if index < length - 1 and filter_ports[index] + 1 == filter_ports[index + 1]:
            end = filter_ports[index + 1]
        else:
            if end - 1 > start:
                result.append(str(start) + ":" + str(end))

            else:
                result.append(str(start))
            start, end = 0, 0
        index += 1

    return result
