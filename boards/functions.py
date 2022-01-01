import random
import string


def random_string_generator(size=10,
                            chars=string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def unique_property_ref_generator(instance):
    new_property_ref = random_string_generator()

    Klass = instance.__class__

    qs_exists = Klass.objects.filter(
                    propertyref=new_property_ref).exists()
    if qs_exists:
        return unique_property_ref_generator(instance)
    return new_property_ref
