if self.map == 2:
    if time.time() - self.start < 3:
        continue

    if position[1] < 200 or (position[1]>650 and position[0]!=60):
        if data is not None:
            x, y = self.lidar_cord(data)
            self.work(x, y)


    else:
        if len(crosswalk_position) != 0:
            if position[0] == 60:
                index = crosswalk_position.index((60, 400))
                if position[1] > 470:
                    self.up(5)
                elif crosswalk_color[index] == 'green' and crosswalk_time[index]>30:
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

            elif 120<position[0]<240:
                if position[1]<300:
                    #두번째 신호등
                    index = crosswalk_position.index((180, 300))
                    if position[1] < 250: # 신호등 전 지점
                        self.up(5)
                        if deg!=0:
                            if deg>-180:
                                self.right(4)
                            else:
                                self.left(4)
                    elif crosswalk_color[index]=='red' or crosswalk_time[index]<15:
                        speed = self.database.car.speed
                        if speed>4:
                            self.down(5)
                        else:
                            self.down(speed)
                    else:
                        self.up(2)

                elif position[1]<490 and position[1]>380:
                    #세번째 신호등
                    index = crosswalk_position.index((180, 500))
                    if position[1] < 440: # 신호등 전 지점
                        self.up(5)
                        if deg!=0:
                            if deg>-180:
                                self.right(2)
                            else:
                                self.left(2)
                    elif crosswalk_color[index] == 'green' and crosswalk_time[index]>10:
                        self.up(5)
                        if deg!=0:
                            if deg>-180:
                                self.right(2)
                            else:
                                self.left(2)

                    elif crosswalk_color[index] == 'green' and crosswalk_time[index]>5 and self.database.car.speed>10:
                        self.up(5)
                        if deg!=0:
                            if deg>-180:
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

            elif 240<position[0]<360:

                if position[1]>570:

                    #4번째 신호등
                    index = crosswalk_position.index((300, 600))
                    if position[1] > 650: # 신호등 전 지점
                        self.up(5)
                        if deg!=0:
                            if deg>0:
                                self.right(5)
                            else:
                                self.left(5)

                    elif crosswalk_color[index] == 'green' and crosswalk_time[index]>10:
                        self.up(5)
                        if deg!=0:
                            if deg>0:
                                self.right(5)
                            else:
                                self.left(5)

                    elif crosswalk_color[index] == 'green' and crosswalk_time[index]>5 and self.database.car.speed>10:
                        self.up(5)
                        if deg!=0:
                            if deg>0:
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
                        if speed>4:
                            self.down(5)
                        else:
                            self.down(speed)
                else:
                    #5번째 신호등
                    index = crosswalk_position.index((300, 200))
                    if position[1] > 300: # 신호등 전 지점
                        self.up(4)
                        if deg != 0:
                            if deg > 0:
                                self.right(5)
                            else:
                                self.left(5)
                    elif crosswalk_color[index] == 'green' and crosswalk_time[index]>10:
                        self.up(4)
                        if deg != 0:
                            if deg > 0:
                                self.right(5)
                            else:
                                self.left(5)

                    elif crosswalk_color[index] == 'green' and crosswalk_time[index]>5 and self.database.car.speed>10:
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

                        elif 360<position[0]<480:
                            #4번째줄, 6번째 신호등

                            index = crosswalk_position.index((420, 400))
                            if position[1] < 340: # 신호등 전 지점
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
                            elif position[1]<410:
                                speed = self.database.car.speed
                                if speed > 4:
                                    self.down(5)
                                else:
                                    self.down(speed)
                            else: self.up(5)

                        elif 480<position[0]<600:
                            if position[1]>570:

                                #7번째 신호등
                                index = crosswalk_position.index((540, 600))
                                if position[1] > 650: # 신호등 전 지점
                                    self.up(5)
                                    if deg!=0:
                                        if deg>0:
                                            self.right(5)
                                        else:
                                            self.left(5)
                                elif crosswalk_color[index] == 'green' and crosswalk_time[index]>10:
                                    self.up(5)
                                    if deg!=0:
                                        if deg>0:
                                            self.right(5)
                                        else:
                                            self.left(5)

                                elif crosswalk_color[index] == 'green' and crosswalk_time[index]>5 and self.database.car.speed>10:
                                    self.up(5)
                                    if deg!=0:
                                        if deg>0:
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
                                    if speed>4:
                                        self.down(5)
                                    else:
                                        self.down(speed)
                            else:
                                #8번째 신호등
                                index = crosswalk_position.index((540, 200))
                                if position[1] > 300: # 신호등 전 지점
                                    self.up(4)
                                    if deg != 0:
                                        if deg > 0:
                                            self.right(5)
                                        else:
                                            self.left(5)
                                elif crosswalk_color[index] == 'green' and crosswalk_time[index]>10:
                                    self.up(4)
                                    if deg != 0:
                                        if deg > 0:
                                            self.right(5)
                                        else:
                                            self.left(5)

                                elif crosswalk_color[index] == 'green' and crosswalk_time[index]>5 and self.database.car.speed>15:
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

                        elif 600<position[0]<720:
                            if position[1]<300:
                                #9번째 신호등
                                index = crosswalk_position.index((660, 300))
                                if position[1] < 250: # 신호등 전 지점
                                    self.up(5)
                                    if deg!=0:
                                        if deg>-180:
                                            self.right(4)
                                        else:
                                            self.left(4)
                                elif crosswalk_color[index]=='red' or crosswalk_time[index]<15:
                                    speed = self.database.car.speed
                                    if speed>4:
                                        self.down(5)
                                    else:
                                        self.down(speed)
                                else:
                                    self.up(2)


                            elif position[1]<490 and position[1]>380:
                                #10번째 신호등
                                index = crosswalk_position.index((660, 500))
                                if position[1] < 440: # 신호등 전 지점
                                    self.up(5)
                                    if deg!=0:
                                        if deg>-180:
                                            self.right(2)
                                        else:
                                            self.left(2)
                                elif crosswalk_color[index] == 'green' and crosswalk_time[index]>15:
                                    self.up(5)
                                    if deg!=0:
                                        if deg>-180:
                                            self.right(2)
                                        else:
                                            self.left(2)

                                elif crosswalk_color[index] == 'green' and crosswalk_time[index]>10 and self.database.car.speed>10:
                                    self.up(5)
                                    if deg!=0:
                                        if deg>-180:
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


                        elif 720<position[0]<840:
                            #마지막!!
                            index = crosswalk_position.index((780, 400))
                            if position[1] > 470:
                                self.up(5)
                                if deg != 0:
                                    if deg > 0:
                                        self.right(5)
                                    else:
                                        self.left(5)
                            elif crosswalk_color[index] == 'green' and crosswalk_time[index] > 15:
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