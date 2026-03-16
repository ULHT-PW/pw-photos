# Galeria de fotografias

### Descrição 
   * Web App em Django que permite inserir, listar e destruir imagens numa base de dados, através de operações CRUD.
   * Alojamento de fotografias em Cloudinary
   * Utilização do package django-cloudinary-storage ([video tutorial](https://www.youtube.com/watch?v=m5O4sSVbzjw))
   * pasta barcos com fotografias de barcos para carregar a sua aplicação
   * aplicação a correr no [Heroku](https://pictures-django-app.herokuapp.com/). Para configurar a sua, siga os passos neste [link](https://github.com/ULHT-PW-2020-21/pw-deployment)

### Requisitos
   * na consola, clonar projeto usando comando `git clone https://github.com/ULHT-PW-2020-21/pw-images`
   * criar ambiente virtual com comando `python -m virtualenv venv`
   * ativar o ambiente virtual com comando  `venv\Scripts\activate`
   * instalar os packages necessários executando comando `python -m pip install -r requirements.txt`
   * lançar a aplicação com comando `python manage.py runserver`

# Preparativos

descreve-se aqui uma implementação básica. A versão implementada tem mais detalhes que depois pode implementar numa segunda fase.

### Scripts no terminal

* deve instalar o modulo `pipenv install django-cloudinary-storage`

#### usando pipenv

```console
mkdir project_pictures
cd project_pictures
pipenv install django
django-admin startproject config .
py manage.py startapp pictures
pipenv install django-cloudinary-storage
pipenv install Pillow
```
notas:
* usamos o package [django-cloudinary-storage](https://github.com/klis87/django-cloudinary-storage) que permite usar ImageField que guardam a imagem em Cloudinary
* Pillow permite usar ImageField
* guarda-se em requirements.txt os packages instalados em [venv](https://docs.python.org/3/tutorial/venv.html). 

<!--

#### usando venv:
```console
mkdir project_pictures
cd project_pictures
python -m virtualenv venv
venv\Scripts\activate
pip install django
django-admin startproject config .
py manage.py startapp pictures
pip install django-cloudinary-storage     # ou pipenv install django-cloudinary-storage
pip install Pillow
pip > freeze requirements.txt 
```
notas:
* usamos o package [django-cloudinary-storage](https://github.com/klis87/django-cloudinary-storage) que permite usar ImageField que guardam a imagem em Cloudinary
* Pillow permite usar ImageField
* guarda-se em requirements.txt os packages instalados em [venv](https://docs.python.org/3/tutorial/venv.html). 


-->

### Criação de conta em [cloudinary.com](https://cloudinary.com/)
* criar conta em cloudinary 
* product: programmable media
* ir a dashboard onde se visualizam as configurações

### settings.py 
* em INSTALLED_APPS, adicionar 
```Python
INSTALLED_APPS += [
   'cloudinary_storage',
   'cloudinary',
   '<nome da aplicação criada>'
]
```
* incluir, no final do ficheiro, as credenciais da conta no cloudinary:
```python
CLOUDINARY_STORAGE = {
  'CLOUD_NAME': "your_Cloud_name",
  'API_KEY': "your_api_key",
  'API_SECRET': "your_api_secret",
}
```
   * na conta do cloudinary.com, no Dashboard, ir buscar os dados cloud_name, api_key, api_secret
   
* especificar nome da pasta a criar no cloudinary para guardar ficheiros da aplicação
```
MEDIA_URL = '/<nome da aplicaçao>/'

DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'
```
# Criação de classe Picture

### models.py

criar classe `Picture` para as imagens, usando ImageField e especificando o nome da pasta no cloudinary onde as imagens devem ser guardadas (dentro da pasta especificada em MEDIA_URL)
```Python
from django.db import models

class Picture(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='pictures/', blank=True)
```

### admin.py
registar no admin o modelo Picture para podermos manipular na app admin

### terminal
```console
py manage.py makemigrations
py manage.py migrate
py manage.py createsuperuser
```

### aplicação admin

* abrir aplicação admin, em 127.0.0.1/admin
* criar/carregar algumas fotos através do modo admin
* ver que no cloudinary ficaram carregadas. 
* se, no model, mudarmos o valor de `upload_to` no `ImageField`, no cloudinary será criada uma nova pasta com esse nome

# Consulta de elementos da base de dados (Read)

### views.py

criamos view index()
```python
from .models import Picture

def index(request):
    pictures = Picture.objects.all()
    ctx = {'pictures': pictures}
    return render(request, 'templates/media/index.html', ctx)
```

### index.html
* criamos pasta templates/media/
* criamos ficheiro index.html, com ciclo para incluir todas as fotos e seus nomes. Atenção, deve incluir a extensão **`.url`**
```html
<body>
    <h1>Pictures</h1>
    {% for picture in pictures %}
        <img src="{{ picture.image.url }}">
        <h4>{{ picture.name }}</h4>
    {% endfor %}
</body>
```

### urls.py
* no config/urls.py, associamos à rota '' os urls de media.urls
    path('', include('media.urls'))
* no media/urls.py, criamos rota do url para a view index
```python
from django.urls import path
from . import views

app_name = 'media'
urlpatterns = [
    path('', views.index, name='index')
]
```

# Criação de novo elemento na base de dados (Create)

### forms.py
criar formulário para nova imagem 

```python
from django import forms
from .models import Picture

class PictureForm(forms.ModelForm):
    class Meta:
        model = Picture
        fields = '__all__'
```

### views.py
criar view para fazer upload de imagem

```python
def upload(request):
    if request.method == 'POST':
        form = PictureForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect(reverse('index'))

    form = PictureForm()
    ctx = {'form': form}
    return render(request, 'media/upload.html', ctx)
```

### upload.html

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Picture</title>
</head>
<body>
    <h2>Upload image</h2>
    <form method="post" enctype="multipart/form-data">
        {% csrf_token %}
        {{ form }}
        <div>
            <br>
            <input type="submit" value="upload image">
        </div>
    </form>
</body>
</html>
```


### urls.py
* em media/urls.py, criar rota do url load/ para a view load()
```python
urlpatterns += [
    path('load/', views.load, name='load')
]
```

# Destruição de elemento da base de dados (Delete)

### index.html
colocar no final das fotos, um link para carregar imagens
```html
<a href="{% url 'media:upload' %}">Carregar imagem</a>
```
colocar, para cada imagem, hiperlink para apagar imagem
```html
(<a href="{% url 'media:delete' picture.pk %}">apagar</a>)
```


### urls.py
* em media/urls.py, criar rota do url delete/picture_pk para a view delete()
```python
urlpatterns += [
    path('delete/<int:picture_pk>', views.delete, name='delete'),
]
```

### views.py
criar view para apagar imagem

```python
def delete(request, picture_pk):
    picture = Picture.objects.get(pk=picture_pk)
    picture.delete()
    return redirect(reverse('media:index'))
```

# Configuração para o ambiente de produção no Heroku
   * Para configurar a aplicação para que corra no Heroku, siga os passos neste [link](https://github.com/ULHT-PW-2020-21/pw-deployment)
