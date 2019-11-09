import time
import pygame
import numpy as np
import math

class Brain:
    def __init__(self, database):
        self.database = database
        self.start = time.time()
        self.map = 0
        self.direction = 0
        self.flag = 0

    def get_v2x_data(self):
        return self.database.v2x_data

    def get_position(self):
        return self.database.car.position

    def get_crosswalk(self):
        v2x = self.get_v2x_data()
        crosswalk_color = []
        crosswalk_position = []
        crosswalk_time = []
        for single_data in v2x.values():
            if single_data[0]=='Crosswalk':
                crosswalk_color.append(single_data[1])
                crosswalk_position.append(single_data[2])
                crosswalk_time.append(single_data[5])

        return crosswalk_color, crosswalk_position,crosswalk_time

    def get_parking(self):
        v2x = self.get_v2x_data()
        mission_check = []
        mission_loc = []
        for data in v2x.values():
            mission_loc.append(data[1])
            mission_check.append(data[4])

        return mission_loc, mission_check

    def mapnum(self):
        v2x = self.get_v2x_data()
        v2x_list = []
        for single_data in v2x.values():
            v2x_list.append(single_data[0])

        mapnum = 0
        if 'Crosswalk' in v2x_list:
            mapnum = 2
        if 'Parking' in v2x_list:
            mapnum = 3
        if 'Left' in v2x_list:
            mapnum = 4
            # 왼쪽이면 0
            self.direction = 0
        if  'Right' in v2x_list:
            mapnum = 4
            # 오른쪽이면 1
            self.direction = 1

        return mapnum

    def get_lidar_data(self):
        # lidar값 가져오기
        data = self.database.lidar.data
        if data is not None:
            data = data[::-1]

        return data

    def lidar_cord(self, data):  # data 인덱스 range는 0부터 179까지입니다
        x = 0
        y = 0

        for i in range(90):
            rad = math.radians(i)
            x += data[i] * np.cos(rad)
            y += data[i] * np.sin(rad)

        for i in range(90, 180):
            rad = math.radians(i)
            x += data[i] * np.cos(rad)
            y += data[i] * np.sin(rad)

        return x, y

    def work(self, x, y):
        MAX = 11458.865
        # Hyper parameters
        k = 5

        r = np.sqrt(x ** 2 + y ** 2)
        thetha = int(np.arctan(x / y) * (180 / np.pi))

        if thetha > 5:
            self.left(5)
        elif 0 < thetha <= 5:
            self.left(5)
        elif thetha < -5:
            self.right(5)
        elif -5 <= thetha <= 0:
            self.right(5)
        else:
            pass

        self.down(abs(thetha) // k)

        p = r / MAX
        v = p * 11 // 1
        dv = v - self.database.car.speed
        # print("DV", dv)

        if dv > 3:
            self.up(3)
        elif 0 < dv <= 3:
            self.up(int(dv))
        elif dv < -3:
            self.down(3)
        elif -3 <= dv < 0:
            self.down(int(dv))
        else:
            pass

    def run(self):
        while True:
            if self.database.stop:
                break

            time.sleep(0.001)
            _ = pygame.event.get()

            '''
            DO NOT CHANGE CODE ABOVE!!!!

            1. How can i get a lidar data?
                data = self.database.lidar.data

            2. How can i move a car?
                self.database.control.up()
                self.database.control.down()
                self.database.control.right()
                self.database.control.left()

                OR

                self.up(num)
                self.down(num)
                self.right(num)
                self.left(num)

                ☆☆☆☆☆ In one loop,
                you can only change the speed up to 5 and the angle up to 8!!

            3. How can i get a car status data?
                self.database.car.direction
                self.database.car.speed

            4. How can i get a v2x data?
                self.database.v2x_data
            '''

            # Implement Your Algorithm HERE!!
            crosswalk_color, crosswalk_position, crosswalk_time = self.get_crosswalk()
            flag = 0

            if time.time()-self.start<5:
                self.map = self.mapnum()
                # print(self.map)

            deg = self.database.car.direction
            position = self.get_position()
            data = self.get_lidar_data()
            v2x = self.get_v2x_data()

            if self.map == 2:

                if self.map == 2:
                    tim = time.time()
                    if time.time() - self.start < 4:
                        continue

                    if position[1] < 200 or (position[1] > 650 and position[0] != 60):
                        if data is not None:
                            x, y = self.lidar_cord(data)
                            self.work(x, y)

                    else:
                        if len(crosswalk_position) != 0:
                            if position[0] == 60:
                                index = crosswalk_position.index((60, 400))
                                if position[1] > 470:
                                    self.up(5)
                                elif crosswalk_color[index] == 'green' and crosswalk_time[index] > 30:
                                    self.up(5)

                                elif crosswalk_color[index] == 'green' and crosswalk_time[
                                    index] > 5 and self.database.car.speed > 10:
                                    self.up(5)

                                elif crosswalk_color[index] == 'red' and self.get_position()[1] < 470:
                                    speed = self.database.car.speed
                                    if speed > 4:
                                        self.down(5)
                                    else:
                                        self.down(speed)

                            elif 120 < position[0] < 240:
                                if position[1] < 300:
                                    # 두번째 신호등
                                    index = crosswalk_position.index((180, 300))
                                    if position[1] < 250:  # 신호등 전 지점
                                        self.up(5)
                                        if deg != 0:
                                            if deg > -180:
                                                self.right(4)
                                            else:
                                                self.left(4)
                                    elif (crosswalk_color[index] == 'red' or crosswalk_time[index] < 15) and flag == 0:

                                        speed = self.database.car.speed
                                        if speed > 4:
                                            self.down(5)
                                        else:
                                            self.down(speed)
                                    else:
                                        self.up(2)
                                        flag = 1

                                elif position[1] < 490 and position[1] > 380:
                                    # 세번째 신호등
                                    index = crosswalk_position.index((180, 500))
                                    if position[1] < 440:  # 신호등 전 지점
                                        self.up(5)
                                        if deg != 0:
                                            if deg > -180:
                                                self.right(2)
                                            else:
                                                self.left(2)
                                    elif crosswalk_color[index] == 'green' and crosswalk_time[index] > 10:
                                        self.up(5)
                                        if deg != 0:
                                            if deg > -180:
                                                self.right(2)
                                            else:
                                                self.left(2)

                                    elif crosswalk_color[index] == 'green' and crosswalk_time[
                                        index] > 5 and self.database.car.speed > 10:
                                        self.up(5)
                                        if deg != 0:
                                            if deg > -180:
                                                self.right(2)
                                            else:
                                                self.left(2)

                                    elif crosswalk_color[index] == 'red' and self.get_position()[1] < 450:
                                        speed = self.database.car.speed
                                        if speed > 4:
                                            self.down(5)
                                        else:
                                            self.down(speed)

                                    else:
                                        speed = self.database.car.speed
                                        if speed > 4:
                                            self.down(5)
                                        else:
                                            self.down(speed)
                                else:
                                    self.up(4)
                                    if deg > -180:
                                        self.right(2)
                                    else:
                                        self.left(2)

                            elif 240 < position[0] < 360:

                                if position[1] > 570:

                                    # 4번째 신호등
                                    index = crosswalk_position.index((300, 600))
                                    if position[1] > 650:  # 신호등 전 지점
                                        self.up(5)
                                        #############################################################3
                                        if deg != 0:
                                            if deg > 0:
                                                self.right(5)
                                            else:
                                                self.left(5)
                                                ###################################################################
                                    elif crosswalk_color[index] == 'green' and crosswalk_time[index] > 10:
                                        self.up(5)
                                        if deg != 0:
                                            if deg > 0:
                                                self.right(5)
                                            else:
                                                self.left(5)

                                    elif crosswalk_color[index] == 'green' and crosswalk_time[
                                        index] > 5 and self.database.car.speed > 10:
                                        self.up(5)
                                        if deg != 0:
                                            if deg > 0:
                                                self.right(5)
                                            else:
                                                self.left(5)

                                    elif crosswalk_color[index] == 'red' and self.get_position()[1] > 650:
                                        speed = self.database.car.speed
                                        if speed > 4:
                                            self.down(5)
                                        else:
                                            self.down(speed)

                                    else:
                                        speed = self.database.car.speed
                                        if speed > 4:
                                            self.down(5)
                                        else:
                                            self.down(speed)
                                else:
                                    # 5번째 신호등
                                    index = crosswalk_position.index((300, 200))
                                    if position[1] > 300:  # 신호등 전 지점
                                        self.up(4)
                                        if deg != 0:
                                            if deg > 0:
                                                self.right(5)
                                            else:
                                                self.left(5)
                                    elif crosswalk_color[index] == 'green' and crosswalk_time[index] > 10:
                                        self.up(4)
                                        if deg != 0:
                                            if deg > 0:
                                                self.right(5)
                                            else:
                                                self.left(5)

                                    elif crosswalk_color[index] == 'green' and crosswalk_time[
                                        index] > 5 and self.database.car.speed > 10:
                                        self.up(4)
                                        if deg != 0:
                                            if deg > 0:
                                                self.right(5)
                                            else:
                                                self.left(5)

                                    elif crosswalk_color[index] == 'red' and self.get_position()[1] > 250:
                                        speed = self.database.car.speed
                                        if speed > 4:
                                            self.down(5)
                                        else:
                                            self.down(speed)
                                    else:
                                        speed = self.database.car.speed
                                        if speed > 4:
                                            self.down(5)
                                        else:
                                            self.down(speed)

                            elif 360 < position[0] < 480:
                                # 4번째줄, 6번째 신호등

                                index = crosswalk_position.index((420, 400))
                                if position[1] < 340:  # 신호등 전 지점
                                    self.up(5)
                                    if deg != 0:
                                        if deg > -180:
                                            self.right(2)
                                        else:
                                            self.left(2)
                                elif crosswalk_color[index] == 'green' and crosswalk_time[index] > 15:
                                    self.up(5)
                                    if deg != 0:
                                        if deg > -180:
                                            self.right(2)
                                        else:
                                            self.left(2)
                                elif position[1] < 410:
                                    speed = self.database.car.speed
                                    if speed > 4:
                                        self.down(5)
                                    else:
                                        self.down(speed)
                                else:
                                    self.up(5)

                            elif 480 < position[0] < 600:
                                if position[1] > 570:

                                    # 7번째 신호등
                                    index = crosswalk_position.index((540, 600))
                                    if position[1] > 650:  # 신호등 전 지점
                                        self.up(5)
                                        #############################################################3
                                        if deg != 0:
                                            if deg > 0:
                                                self.right(5)
                                            else:
                                                self.left(5)
                                                ###################################################################
                                    elif crosswalk_color[index] == 'green' and crosswalk_time[index] > 10:
                                        self.up(5)
                                        if deg != 0:
                                            if deg > 0:
                                                self.right(5)
                                            else:
                                                self.left(5)

                                    elif crosswalk_color[index] == 'green' and crosswalk_time[
                                        index] > 5 and self.database.car.speed > 10:
                                        self.up(5)
                                        if deg != 0:
                                            if deg > 0:
                                                self.right(5)
                                            else:
                                                self.left(5)

                                    elif crosswalk_color[index] == 'red' and self.get_position()[1] > 650:
                                        speed = self.database.car.speed
                                        if speed > 4:
                                            self.down(5)
                                        else:
                                            self.down(speed)

                                    else:
                                        speed = self.database.car.speed
                                        if speed > 4:
                                            self.down(5)
                                        else:
                                            self.down(speed)
                                else:
                                    # 8번째 신호등
                                    index = crosswalk_position.index((540, 200))
                                    if position[1] > 300:  # 신호등 전 지점
                                        self.up(4)
                                        if deg != 0:
                                            if deg > 0:
                                                self.right(5)
                                            else:
                                                self.left(5)
                                    elif crosswalk_color[index] == 'green' and crosswalk_time[index] > 10:
                                        self.up(4)
                                        if deg != 0:
                                            if deg > 0:
                                                self.right(5)
                                            else:
                                                self.left(5)

                                    elif crosswalk_color[index] == 'green' and crosswalk_time[
                                        index] > 5 and self.database.car.speed > 15:
                                        self.up(4)
                                        if deg != 0:
                                            if deg > 0:
                                                self.right(5)
                                            else:
                                                self.left(5)

                                    elif crosswalk_color[index] == 'red' and self.get_position()[1] > 250:
                                        speed = self.database.car.speed
                                        if speed > 4:
                                            self.down(5)
                                        else:
                                            self.down(speed)
                                    else:
                                        speed = self.database.car.speed
                                        if speed > 4:
                                            self.down(5)
                                        else:
                                            self.down(speed)

                            elif 600 < position[0] < 720:
                                if position[1] < 300:
                                    # 9번째 신호등
                                    index = crosswalk_position.index((660, 300))
                                    if position[1] < 250:  # 신호등 전 지점
                                        self.up(5)
                                        if deg != 0:
                                            if deg > -180:
                                                self.right(4)
                                            else:
                                                self.left(4)
                                    elif crosswalk_color[index] == 'red' or crosswalk_time[index] < 15:
                                        speed = self.database.car.speed
                                        if speed > 4:
                                            self.down(5)
                                        else:
                                            self.down(speed)
                                    else:
                                        self.up(2)


                                elif position[1] < 490 and position[1] > 380:
                                    # 10번째 신호등
                                    index = crosswalk_position.index((660, 500))
                                    if position[1] < 440:  # 신호등 전 지점
                                        self.up(5)
                                        if deg != 0:
                                            if deg > -180:
                                                self.right(2)
                                            else:
                                                self.left(2)
                                    elif crosswalk_color[index] == 'green' and crosswalk_time[index] > 20:
                                        self.up(5)
                                        if deg != 0:
                                            if deg > -180:
                                                self.right(2)
                                            else:
                                                self.left(2)

                                    elif crosswalk_color[index] == 'green' and crosswalk_time[
                                        index] > 10 and self.database.car.speed > 10:
                                        self.up(5)
                                        if deg != 0:
                                            if deg > -180:
                                                self.right(2)
                                            else:
                                                self.left(2)

                                    elif crosswalk_color[index] == 'red' and self.get_position()[1] < 450:
                                        speed = self.database.car.speed
                                        if speed > 4:
                                            self.down(5)
                                        else:
                                            self.down(speed)

                                    else:
                                        speed = self.database.car.speed
                                        if speed > 4:
                                            self.down(5)
                                        else:
                                            self.down(speed)
                                else:
                                    self.up(4)
                                    if deg > -180:
                                        self.right(2)
                                    else:
                                        self.left(2)


                            elif 720 < position[0] < 840:
                                # 마지막!!
                                index = crosswalk_position.index((780, 400))
                                if position[1] > 470:
                                    self.up(5)
                                    if deg != 0:
                                        if deg > 0:
                                            self.right(5)
                                        else:
                                            self.left(5)
                                elif crosswalk_color[index] == 'green' and crosswalk_time[index] > 20:
                                    self.up(5)
                                    if deg != 0:
                                        if deg > 0:
                                            self.right(5)
                                        else:
                                            self.left(5)

                                elif crosswalk_color[index] == 'red' and self.get_position()[1] < 470:
                                    speed = self.database.car.speed
                                    if speed > 4:
                                        self.down(5)
                                    else:
                                        self.down(speed)
                                else:
                                    speed = self.database.car.speed
                                    if speed > 4:
                                        self.down(5)
                                    else:
                                        self.down(speed)

            elif self.map == 3:
                current_speed = self.database.car.speed
                parking_loc, parking_suc = self.get_parking()
                # print(position)

                if self.flag==3:
                    if data is not None:
                        x, y = self.lidar_cord(data)
                        self.work(x, y)

                        if position[0]<440 and position[1]>120:
                            self.flag=1

                if self.flag==5:
                    if data is not None:
                        x, y = self.lidar_cord(data)
                        self.work(x, y)

                        if position[0]>340 and position[1]>400:
                            self.flag=1

                if self.flag==6:
                    if data is not None:
                        data[150:180] = 40
                        x, y = self.lidar_cord(data)
                        self.work(x, y)

                if position[0] > 440:
                    if position[0] == 500 and position[1]>370:
                        self.up(5)

                    elif self.flag==1:
                        index = parking_loc.index((560, 300))
                        if position[0] < 568:
                            self.up(1)
                        else:
                            if current_speed > 0:
                                self.down(current_speed)
                        if parking_suc[index] is True:
                            self.flag = 2

                    elif self.flag==2:
                        if position[0]>500:
                            self.down(2)
                        else:
                            self.up(5)
                            self.left(8)
                            if -5 < deg < 5:
                                self.flag = 3

                    # elif self.flag==3:

                    elif position[1] < 370:
                        if current_speed > 5 and deg == 0:
                            self.down(5)

                        elif current_speed > 0 and deg == 0:
                            self.down(current_speed)

                        elif current_speed > 0 and deg != 0 and position[0]>586:
                            self.down(2)

                        elif current_speed == 0:
                            if deg>-90:
                                self.right(8)
                            else:
                                self.flag = 1

                elif position[0] < 440 and position[1]<400:
                    if self.flag==1:
                        if position[1] > 220:
                            if current_speed>5:
                                self.down(5)

                            elif current_speed>0:
                                self.down(current_speed)

                            elif current_speed==0:
                                if deg>92:
                                    self.right(8)
                                else:
                                    self.right(10)
                                    self.flag=2

                    if self.flag==2:
                        index = parking_loc.index((220, 200))
                        if position[0]>290:
                            self.up(1)
                        else:
                            if current_speed > 0:
                                self.down(current_speed)
                            if parking_suc[index] is True:
                                self.flag = 4

                    if self.flag==4:
                        # angle check
                        if position[0]<320:
                            self.down(1)
                        else:
                            self.down(1)
                            self.left(8)
                            if position[0]>390 and position[1]<190:
                                self.flag=5

                elif position[0] < 440 and position[1]>400:
                    if self.flag==1:
                        if position[1] > 520:
                            if current_speed>5:
                                self.down(5)

                            elif current_speed>0:
                                self.down(current_speed)

                            elif current_speed==0:
                                if deg>92:
                                    self.right(8)
                                else:
                                    self.right(10)
                                    self.flag=2

                    if self.flag==2:
                        index = parking_loc.index((220, 500))
                        if position[0]>300:
                            self.up(1)
                        else:
                            if current_speed > 0:
                                self.down(current_speed)
                            if parking_suc[index] is True:
                                self.flag = 4

                    if self.flag==4:
                        # angle check
                        if position[0]<320:
                            self.down(1)
                        else:
                            self.down(1)
                            self.left(8)
                            if position[0]>370 and position[1]<480:
                                self.flag=6

            elif self.map==4:
                if data is not None:
                    if position[1]>580:
                        # 조향
                        if self.direction==1:
                            #오른쪽이면 1
                            if position[0]<650:
                                data[0:20]=20
                            x, y = self.lidar_cord(data)
                            self.work(x, y)

                        elif self.direction==0:
                            #왼쪽이면 0
                            if position[0]>350:
                                data[160:180]=20
                            x, y = self.lidar_cord(data)
                            self.work(x, y)
                    else:

                        if position[0]<120 and position[1]>100:

                            # 신호등
                            if deg > 0:
                                self.right(5)
                            elif deg < 0:
                                self.left(5)

                            # 왼쪽
                            crosswalk_color, crosswalk_position, crosswalk_time = self.get_crosswalk()

                            if position[1]>500:
                                if (50,500) in crosswalk_position:
                                    index = crosswalk_position.index((50, 500))
                                    speed = self.database.car.speed
                                    if crosswalk_color[index]=='red':
                                        if speed>1:
                                            self.down(1)
                                    else:
                                        self.up(5)

                            elif position[1]>400:
                                if (50,400) in crosswalk_position:
                                    index = crosswalk_position.index((50, 400))
                                    speed = self.database.car.speed
                                    if crosswalk_color[index]=='red':
                                        if speed>1:
                                            self.down(1)
                                    else:
                                        self.up(5)

                            elif position[1]>300:
                                if (50,400) in crosswalk_position:
                                    index = crosswalk_position.index((50, 300))
                                    speed = self.database.car.speed

                                    if crosswalk_color[index]=='red':
                                        if speed>1:
                                            self.down(1)
                                    else:
                                        self.up(5)

                            elif position[1]>200:
                                if (50,400) in crosswalk_position:
                                    index = crosswalk_position.index((50, 200))
                                    speed = self.database.car.speed

                                    if crosswalk_color[index]=='red':
                                        if speed>1:
                                            self.down(1)
                                    else:
                                        self.up(5)

                        elif position[0]>880 and position[1]>100:

                            # 신호등
                            if deg > 0:
                                self.right(5)
                            elif deg < 0:
                                self.left(5)

                            # 오른쪽
                            crosswalk_color, crosswalk_position, crosswalk_time = self.get_crosswalk()

                            if position[1]>500:
                                if (950,500) in crosswalk_position:
                                    index = crosswalk_position.index((950, 500))
                                    speed = self.database.car.speed
                                    if crosswalk_color[index]=='red':
                                        if speed>1:
                                            self.down(1)
                                    else:
                                        self.up(5)

                            elif position[1]>400:
                                if (950,400) in crosswalk_position:
                                    index = crosswalk_position.index((950, 400))
                                    speed = self.database.car.speed

                                    if crosswalk_color[index]=='red':
                                        if speed>1:
                                            self.down(1)
                                    else:
                                        self.up(5)

                            elif position[1]>300:
                                if (950,400) in crosswalk_position:
                                    index = crosswalk_position.index((950, 300))
                                    speed = self.database.car.speed

                                    if crosswalk_color[index]=='red':
                                        if speed>1:
                                            self.down(1)
                                    else:
                                        self.up(5)

                            elif position[1]>200:
                                if (950,400) in crosswalk_position:
                                    index = crosswalk_position.index((950, 200))
                                    speed = self.database.car.speed

                                    if crosswalk_color[index]=='red':
                                        if speed>1:
                                            self.down(1)
                                    else:
                                        self.up(5)

                        elif 240 < position[0] < 360 and position[1]>100 :

                            # 신호등
                            if deg > 0:
                                self.right(5)
                            elif deg < 0:
                                self.left(5)

                            # 왼쪽
                            crosswalk_color, crosswalk_position, crosswalk_time = self.get_crosswalk()

                            if position[1] > 400:
                                if (250, 400) in crosswalk_position:
                                    index = crosswalk_position.index((250, 400))
                                    speed = self.database.car.speed
                                    if crosswalk_color[index] == 'red':
                                        if speed>1:
                                            self.down(1)
                                    else:
                                        self.up(5)

                            elif position[1] > 200:
                                if (250, 200) in crosswalk_position:
                                    index = crosswalk_position.index((250, 200))
                                    speed = self.database.car.speed

                                    if crosswalk_color[index] == 'red':
                                        if speed<10:
                                            self.down(1)
                                    else:
                                        self.up(5)

                        elif 640 < position[0] < 760 and position[1]>100:

                            # 신호등
                            if deg > 0:
                                self.right(5)
                            elif deg < 0:
                                self.left(5)

                            # 오른쪽
                            crosswalk_color, crosswalk_position, crosswalk_time = self.get_crosswalk()

                            if position[1] > 400:
                                if (750, 400) in crosswalk_position:
                                    index = crosswalk_position.index((750, 400))
                                    speed = self.database.car.speed
                                    if crosswalk_color[index] == 'red':
                                        if speed>1:
                                            self.down(1)
                                    else:
                                        self.up(5)

                            elif position[1] > 200:
                                if (750, 200) in crosswalk_position:
                                    index = crosswalk_position.index((750, 200))

                                    if crosswalk_color[index] == 'red':
                                        if speed<10:
                                            self.down(1)
                                    else:
                                        self.up(5)

                        else:
                            x, y = self.lidar_cord(data)
                            self.work(x, y)

    def up(self, num: int = 1):
        for i in range(num):
            self.database.control.up()

    def down(self, num: int = 1):
        for i in range(num):
            self.database.control.down()

    def right(self, num: int = 1):
        for i in range(num):
            self.database.control.right()

    def left(self, num: int = 1):
        for i in range(num):
            self.database.control.left()
