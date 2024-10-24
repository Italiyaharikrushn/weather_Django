from django.shortcuts import render, redirect
import requests

def home(request):
    data = {}

    if request.method == "POST":
        city = request.POST.get("city", "")

        if city:
            try:
                response = requests.get(
                    f"https://api.openweathermap.org/data/2.5/weather?q={city}&units=metric&appid=88272d6772d73de9bef96cb813e376ea"
                )
                list_of_data = response.json()

                if response.status_code == 200:
                    data = {
                        "city": city,
                        "description": list_of_data["weather"][0]["description"],
                        "icon": list_of_data["weather"][0]["icon"],
                        "temp": list_of_data["main"]["temp"],
                    }
                    return redirect(f'/weather?city={data["city"]}&desc={data["description"]}&icon={data["icon"]}&temp={data["temp"]}')
                else:
                    data["error"] = f"City {city} not found."
                    return redirect(f'/weather?error={data["error"]}')
                    
            except Exception as e:
                data["error"] = "An error occurred while fetching the weather data."
                return redirect(f'/weather?error={data["error"]}')
    
    elif request.method == "GET":
        city = request.GET.get("city")
        description = request.GET.get("desc")
        icon = request.GET.get("icon")
        temp = request.GET.get("temp")
        error = request.GET.get("error")

        if city and description and icon and temp:
            data = {
                "city": city,
                "description": description,
                "icon": icon,
                "temp": temp,
            }
        elif error:
            data["error"] = error

    return render(request, "weatherapp/index.html", data)
