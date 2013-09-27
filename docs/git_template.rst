Git Template Repository
=======================

Now django-deployer supports templating by fetching from remote git repository, to create a new provider class, you could implement a new class which inherits to ``django_deployer.providers.PaaSProvider``.

The only two attributes that does matter is ``git_template`` and ``git_template_url``, you should define the provider class as following:


.. code:: python


    class YourProvider(PaaSProvider):
        name = 'yourprovider'

        PYVERSIONS = {
            "Python2.7": "v2.7"
        }

        setup_instruction = """
    the instruction which will show up after setup
        """

        git_template = True
        git_template_url = "<your-provider-repo-url>"


