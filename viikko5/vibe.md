# GitHub Copilotin koodaama web-käyttöliittymä Ohtuvarastolle

https://github.com/ARomppainen/ohtuvarasto/pull/2

Copilotin generoima koodi oli toimivaa. Selvästi se pystyy hyvin tämmöiseen
'boilerplaten' generointiin. Promptaus toimi sekä suomeksi ja englanniksi.

Generoitu koodi oli suhteellisen selkeää. Esim html-templatet oli nimetty
kuvaavasti. Yhtään apufunktiota / metodia en nähnyt. Koodin termit ovat sekaisin
suomea ja englantia. En kokeillut olisiko Copilot onnistunut nimeämään kaiken
suomeksi...

Pyysin Copilotia refaktoroimaan "in-memory database"-ratkaisun erilliseen
luokkaan ja käyttämään repository-patternia. Se onnistui luomaan abstraktin
WarehouseRepository-luokan ja sille toteutuksen. Tämän toteutusen 'wiring' jäi
kuitenkin app.py moduuliin ja in-memory toteutukseen on edelleen vahva
riippuvuus generoiduissa testeissä.

En sinänsä oppinut uutta Copilotin koodista, mutta opin paljon siitä mihin se
pystyy.
