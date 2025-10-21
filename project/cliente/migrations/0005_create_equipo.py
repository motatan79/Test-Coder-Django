from django.db import migrations, models


def create_calcio(apps, schema_editor):
    Equipo = apps.get_model('cliente', 'Equipo')
    Pais = apps.get_model('cliente', 'Pais')
    # Buscar un país existente o crear uno por defecto
    pais = Pais.objects.first()
    if not pais:
        pais = Pais.objects.create(nombre='Desconocido', codigo='XX')
    Equipo.objects.create(nombre='Calcio', pais=pais)


class Migration(migrations.Migration):

    dependencies = [
        ('cliente', '0004_alter_cliente_fecha_nacimiento'),
    ]

    operations = [
        migrations.CreateModel(
            name='Equipo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100, unique=True)),
                ('pais', models.ForeignKey(on_delete=models.deletion.CASCADE, to='cliente.pais')),
            ],
        ),
        migrations.RunPython(create_calcio),
    ]
