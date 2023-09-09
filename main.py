import datetime
from pprint import pprint
import plotly.express as px
import pandas as pd
import plotly.figure_factory as ff


class ShipTraffic:
    def parse_reqs(self, reqs):  # функция перебора заявок
        resp = list(map(lambda x: self.processing_req(x),
                        sorted(reqs, key=lambda x: (datetime.datetime.strptime(x[6], '%d.%m.%Y %H:%M'),
                                                    datetime.datetime.strptime(x[7], '%d.%m.%Y %H:%M')))))
        self.made_gant(resp)

    def processing_req(self, req):  # функция обработки заявки
        req[6] = datetime.datetime.strptime(req[6], '%d.%m.%Y %H:%M')
        req[7] = datetime.datetime.strptime(req[7], '%d.%m.%Y %H:%M')
        time_interval = self.ship_graph_time(req)
        route = self.can_swim(time_interval, req)
        return route

    def ship_graph_time(self, req):  # функция определения временного интервала для ребра: [rebro, time_start, time_end]
        from data import routes
        rout1, rout2 = routes[req[4] + req[5]]
        time_rout1, time_rout2 = self.time_route_maker(rout1, req), self.time_route_maker(rout2, req)
        return [time_rout1, time_rout2]

    def can_swim(self, time_interval, req):  # функция определения плотности льда на пути транспортного судна
        swim_route_1, swim_route_2 = self.ice_density(time_interval[0], req[2]), self.ice_density(time_interval[1],
                                                                                                  req[2])
        if swim_route_1 != 403 and swim_route_2 != 403:
            optimal = sorted([swim_route_1, swim_route_2], key=lambda x: x[-1][2])[0]
        elif swim_route_1 != 403 or swim_route_2 != 403:
            optimal = swim_route_1 if swim_route_1 != 403 else swim_route_2
        else:
            optimal = [403, sorted([time_interval[0], time_interval[1]], key=lambda x: x[-1][2])[0]]
        return optimal

    @staticmethod
    def ice_density(time_rout, req):  # функция определяет плотность льда и возможность прохождения в n-день
        resp = []  # [rebro, time_start, time_end, status]
        from data import class_can, ice_can, day_ice
        for i in time_rout:
            if i[1].date() == i[2].date():
                weather = day_ice[i[0] - 1][i[1].day - 1 if i[1].day - 1 <= 29 else i[1].day - 2]
                if ice_can[int(weather)][class_can[req]] == '3':
                    return 403
                resp.append([i[0], i[1], i[2], ice_can[int(weather)][class_can[req]]])
            elif i[1].date() + datetime.timedelta(days=1) == i[2].date():
                weather = max([day_ice[i[0] - 1][i[1].day - 1 if i[1].day - 1 <= 29 else i[1].day - 2],
                               day_ice[i[0] - 1][i[2].day - 1 if i[2].day - 1 <= 29 else i[2].day - 2]])
                if ice_can[int(weather)][class_can[req]] == '3':
                    return 403
                resp.append([i[0], i[1], i[2], ice_can[int(weather)][class_can[req]]])
            elif i[1].date() + datetime.timedelta(days=2) == i[2].date():
                weather = max([day_ice[i[0] - 1][i[1].day - 1 if i[1].day - 1 <= 29 else i[1].day - 2],
                               day_ice[i[0] - 1][i[2].day - 1 if i[2].day - 1 <= 29 else i[2].day - 2],
                               day_ice[i[0] - 1][i[2].day - 1]])
                if ice_can[int(weather)][class_can[req]] == '3':
                    return 403
                resp.append([i[0], i[1], i[2], ice_can[int(weather)][class_can[req]]])
        return resp[::-1]

    @staticmethod
    def time_route_maker(rout, req):
        from data import edges
        time_route = []
        for i in rout:
            time_rout = [i]
            time_rout.append(req[6] if rout.index(i) == 0 else time_route[-1][2])
            time_swim = round((edges[i] / (int(req[3]) * 1.852)) * 60)
            time_swim = datetime.timedelta(hours=time_swim // 60, minutes=time_swim - 60 * (time_swim // 60))
            time_rout.append(time_rout[1] + time_swim)
            time_route.append(time_rout)
        return time_route[::-1]

    @staticmethod
    def made_gant(data):
        from data import skip_status
        gant_data = []
        h = 1
        for i in data:
            if i[0] == 403:
                for j in i[1]:
                    gant_data.append(dict(Task=f'Заявка №{str(h)}', Start=j[1], Finish=j[2], Resource=skip_status[3]))
            else:
                for j in i:
                    gant_data.append(
                        dict(Task=f'Заявка №{str(h)}', Start=j[1], Finish=j[2], Resource=skip_status[int(j[-1])]))
            h += 1
        colors = {'Проход невозможен': 'rgb(220, 0, 0)',
                  'Нужна проводка': (1, 0.9, 0.16),
                  'Самостоятельно': 'rgb(0, 255, 100)'}

        fig = ff.create_gantt(gant_data, colors=colors, index_col='Resource', show_colorbar=True,
                              group_tasks=True)
        fig.show()


def main():
    from data import icebreakers_requests

    sd = ShipTraffic()
    sd.parse_reqs(icebreakers_requests)


if __name__ == "__main__":
    main()
