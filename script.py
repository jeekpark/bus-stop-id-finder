import requests
import xml.etree.ElementTree as ET
import os

def refresh():
  clear_console()
  print("\n\033[32m버스 정류소 ID 파인더\033[0m\n")

def clear_console():
    if os.name == 'nt':  # 윈도우즈의 경우
        os.system('cls')
    else:  # 유닉스 기반 시스템의 경우
        os.system('clear')

refresh()

service_key = input("공공데이터 인증키(Decoding) 입력: ")

refresh()

bus_number = input("버스 번호 입력: ")

refresh()

city_name = input("도시 이름 입력(예: 용인): ")

refresh()

url = 'http://apis.data.go.kr/6410000/busrouteservice/getBusRouteList'
params ={'serviceKey' : service_key, 'keyword' : bus_number }

response = requests.get(url, params=params)

root = ET.fromstring(response.content)
bus_routes = []
for bus_route in root.findall(".//busRouteList"):
  route_name = bus_route.find('routeName').text
  region_name = bus_route.find('regionName').text
  route_id = bus_route.find('routeId').text
  if route_name == bus_number and region_name.find(city_name) != -1:
    bus_routes.append((route_name, region_name, route_id))

selected_route = 0
result_route_id = 0
while True:
    # 리스트에 저장된 모든 정보 출력
    for index, route in enumerate(bus_routes):
      print(f"{index + 1}.\t[{route[1]}]")

    try:
        selected_index = int(input('\n번호를 선택하세요: ')) - 1
        if selected_index < 0:
          raise IndexError
        selected_route = bus_routes[selected_index]  # 선택된 노선 정보
        result_route_id = bus_routes[selected_index][2]
        clear_console()
        
        break  # 유효한 선택을 했으므로 반복문 탈출

    except IndexError:
        clear_console()
        print("\n\033[91m잘못된 번호입니다. 올바른 번호를 입력해주사요.\033[0m\n")
    except ValueError:
        clear_console()
        print("\n\033[91m숫자를 입력해야합니다.\033[0m\n")

refresh()

print(f"선택된 노선: {selected_route[0]}({selected_route[1]})\n")
selected_route_id = selected_route[2]

url = 'http://apis.data.go.kr/6410000/busrouteservice/getBusRouteStationList'
params ={'serviceKey' : service_key, 'routeId' : selected_route_id }

response = requests.get(url, params=params)

root = ET.fromstring(response.content)
bus_route_station_list = []
for bus_station in root.findall(".//busRouteStationList"):
  bus_route_station_list.append((bus_station.find('stationSeq').text, bus_station.find('stationName').text, bus_station.find('stationId').text, bus_station.find('turnYn').text))
bus_route_station_list = sorted(bus_route_station_list, key=lambda x: int(x[0]))




# User input for the station name
station_name_to_find = input("노선 내의 정류소 이름 입력: ")
selected_bus_route_station_list = []
for index, station in enumerate(bus_route_station_list):
    if station[1].find(station_name_to_find) != -1:
        # 현재 요소 저장
        current_station = station

        # 직전 요소 저장 (리스트의 첫 번째 요소가 아니면)
        if index > 0:
            previous_station = bus_route_station_list[index - 1]
        else:
            previous_station = None  # 리스트의 시작인 경우

        # 직후 요소 저장 (리스트의 마지막 요소가 아니면)
        if index < len(bus_route_station_list) - 1:
            next_station = bus_route_station_list[index + 1]
        else:
            next_station = None  # 리스트의 끝인 경우

        # 현재, 직전, 직후 요소를 함께 저장
        selected_bus_route_station_list.append((previous_station, current_station, next_station))



result_station_order = 0
result_station_id = 0


while True:
  refresh()
  for index, station in enumerate(selected_bus_route_station_list):
      print(f"{index + 1}.\t", end = "")
      if station[0] == None:
         print("(없음)", end = "")
      else:
         print(station[0][1], end = "")
      
      print(" -> " + station[1][1] + " -> ", end = "")

      if station[2] == None:
         print("(없음)", end = "")
      else:
         print(station[2][1])
  
  try:
    selected_index = int(input('\n버스 방향을 선택하세요: ')) - 1
    if selected_index < 0:
      raise IndexError
    result_station_id = selected_bus_route_station_list[selected_index][1][2]
    result_station_order = selected_bus_route_station_list[selected_index][1][0]
    clear_console()
    break
  except IndexError:
    clear_console()
    print("\n\033[91m잘못된 번호입니다. 올바른 번호를 입력해주사요.\033[0m\n")
  except ValueError:
    clear_console()
    print("\n\033[91m숫자를 입력해야합니다.\033[0m\n")
refresh()
print(f"버스 정류소 ID(stationId):\t{result_station_id}\n")
print(f"버스 노선 ID(routeId):\t\t{result_route_id}\n")
print(f"버스 노선의 순번(staOrder):\t{result_station_order}\n")