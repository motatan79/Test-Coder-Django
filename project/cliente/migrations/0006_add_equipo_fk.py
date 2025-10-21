from django.db import migrations, models


def set_equipo_calcio(apps, schema_editor):
    Equipo = apps.get_model('cliente', 'Equipo')
    Cliente = apps.get_model('cliente', 'Cliente')
    try:
        calcio = Equipo.objects.get(nombre='Calcio')
    except Equipo.DoesNotExist:
        calcio = Equipo.objects.create(nombre='Calcio')
    Cliente.objects.filter(equipo__isnull=True).update(equipo=calcio)


class Migration(migrations.Migration):

    dependencies = [
        ('cliente', '0005_create_equipo'),
    ]

    operations = [
        migrations.AddField(
            model_name='cliente',
            name='equipo',
            field=models.ForeignKey(null=True, blank=True, on_delete=models.deletion.CASCADE, related_name='jugadores', to='cliente.equipo'),
        ),
        migrations.RunPython(set_equipo_calcio),
        migrations.AlterField(
            model_name='cliente',
            name='equipo',
            field=models.ForeignKey(on_delete=models.deletion.CASCADE, related_name='jugadores', to='cliente.equipo'),
        ),
    ]
