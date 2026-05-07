from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User, auth

def home(request):
    return render(request, "index.html")


def login(request):
    if request.method == "POST":
        uname = request.POST['luser'].lower()
        pass1 = request.POST['lpass'].lower()
        user = auth.authenticate(username=uname, password=pass1)

        if user is not None:
            auth.login(request, user)
            return redirect('/')
        else:
            messages.info(request, "Invalid Credentials")
            return render(request, "login.html")

    return render(request, 'login.html')


def register(request):
    if request.method == "POST":
        username = request.POST['user'].lower()
        fname = request.POST['fname'].lower()
        lname = request.POST['lname'].lower()
        email = request.POST['email']
        passwd = request.POST['pass']
        con_passwd = request.POST['confirm_pass']

        if passwd == con_passwd:
            if User.objects.filter(username=username).exists():
                messages.info(request, "Username already exists!")
                return render(request, "register.html")

            elif User.objects.filter(email=email).exists():
                messages.info(request, "Email already exists!")
                return render(request, "register.html")

            else:
                user = User.objects.create_user(
                    username=username,
                    first_name=fname,
                    last_name=lname,
                    email=email,
                    password=passwd
                )
                user.save()
                return redirect('login')
        else:
            messages.info(request, "Passwords do not match!")
            return render(request, "register.html")

    return render(request, "register.html")


def logout(request):
    auth.logout(request)
    return redirect('/')


def fertilizer(request):
    if request.method == "POST":
        import pandas as pd
        import numpy as np
        from sklearn.preprocessing import LabelEncoder
        from sklearn.model_selection import train_test_split
        from sklearn.ensemble import RandomForestClassifier

        try:
            Temparature = float(request.POST['temp'])
            Humidity = float(request.POST['humid'])
            Moisture = float(request.POST['moisture'])

            Soil_Type = request.POST['soil'].strip().title()
            Crop_Type = request.POST['crop'].strip().title()

            Nitrogen = float(request.POST['nitro'])
            Potassium = float(request.POST['potassium'])
            Phosphorous = float(request.POST['phos'])

        except:
            return render(request, "fertilizer.html", {
                "error": "Invalid input! Please enter correct values."
            })

        df = pd.read_csv("static/Dataset/fertilizer.csv")
        df.columns = df.columns.str.strip()

        le_soil = LabelEncoder()
        le_crop = LabelEncoder()

        df['Soil Type'] = le_soil.fit_transform(df['Soil Type'])
        df['Crop Type'] = le_crop.fit_transform(df['Crop Type'])

    
        if Soil_Type not in le_soil.classes_:
            return render(request, "fertilizer.html", {
                "error": f"Soil type '{Soil_Type}' not found in dataset"
            })

        if Crop_Type not in le_crop.classes_:
            return render(request, "fertilizer.html", {
                "error": f"Crop type '{Crop_Type}' not found in dataset"
            })

        soil = le_soil.transform([Soil_Type])[0]
        crop = le_crop.transform([Crop_Type])[0]

        X = df.drop('Fertilizer Name', axis=1)
        y = df['Fertilizer Name']

        x_train, x_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

        model = RandomForestClassifier()
        model.fit(x_train, y_train)

        prediction = model.predict([[
            Temparature, Humidity, Moisture,
            soil, crop, Nitrogen, Potassium, Phosphorous
        ]])[0]

    
        return render(request, "fertilizer.html", {
            "prediction": prediction,
            "temp": Temparature,
            "humid": Humidity,
            "moisture": Moisture,
            "soil": Soil_Type,
            "crop": Crop_Type,
            "nitro": Nitrogen,
            "potassium": Potassium,
            "phos": Phosphorous
        })

    return render(request, "fertilizer.html")


def crop(request):
    if request.method == "POST":
        try:
            nitro = float(request.POST['nitro'])
            phos = float(request.POST['phos'])
            pottas = float(request.POST['pottas'])
            temp = float(request.POST['temp'])
            humid = float(request.POST['humid'])
            ph = float(request.POST['ph'])
            rain = float(request.POST['rain'])
        except:
            return render(request, "crop.html", {"error": "Invalid input"})

        import pandas as pd
        import numpy as np
        from sklearn.model_selection import train_test_split
        from sklearn.ensemble import RandomForestClassifier

        df = pd.read_csv('static/Dataset/Crop_recommendation.csv')

        X = df[['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall']]
        y = df['label']

        Xtrain, Xtest, Ytrain, Ytest = train_test_split(
            X, y, test_size=0.2, random_state=2
        )

        model = RandomForestClassifier(n_estimators=50, random_state=0)
        model.fit(Xtrain, Ytrain)

        data = np.array([[nitro, phos, pottas, temp, humid, ph, rain]])
        prediction = model.predict(data)[0]

        return render(request, "crop_predict.html", {
            "pred": prediction,
            "nitro": nitro,
            "phos": phos,
            "pottas": pottas,
            "temp": temp,
            "humid": humid,
            "ph": ph,
            "rain": rain
        })

    return render(request, "crop.html")


def crop_predict(request):
    return render(request, "crop_predict.html")