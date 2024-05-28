from setuptools import setup, find_packages

setup(
    name='nonebot-plugin-antimonkey',
    version='0.1.0',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'nonebot2',
        'nonebot-adapter-onebot',
        'opencv-python',
        'aiohttp',
        'tensorflow',
        'keras',
        'numpy',
    ],
    entry_points={
        'nonebot.plugin': [
            'nonebot_plugin_antimonkey = nonebot_plugin_antimonkey'
        ]
    },
    package_data={
        'nonebot_plugin_antimonkey': ['py.typed'],
    },
    zip_safe=False,
)
