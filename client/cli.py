# -*- coding: utf-8 -*-

import click
# import logging
from .log import get_log
from .api import Api
from .main import RequestData
import asyncio

def validate_url(ctx, param, value):
    try:
        return value
    except ValueError:
        raise click.BadParameter('url need to be format: tcp://ipv4:port')

@click.command()
@click.option('--url', default='http://192.168.1.162:8088',
              callback=validate_url,
              envvar='Server_url',
              help='Server url, ENV: URL')
@click.option('--port', default=8099,
              envvar='RPS_PORT',
              help='Api port, default=8099, ENV: RPS_PORT')
@click.option('--endpoint', default='v1/cables',
              help='Data Endpoint')
@click.option('--username', default='admin',
              help='login user name')
@click.option('--password', default='admin',
              help='login user password')
@click.option('--debug', is_flag=True)

def main(url, port, endpoint, username, password, debug):
    """Keeper for SAM2"""

    click.echo("See more documentation at http://www.mingvale.com")

    info = {'url': url,
            'port': port,
            'endpoint': endpoint}

    log = get_log(debug)
    log.info('Basic Information: {}'.format(info))

    loop = asyncio.get_event_loop()
    loop.set_debug(0)

    user_info = {"username": username, "password": password}

    try:
       site =  RequestData(url, user_info, loop, endpoint)
       api = Api(loop=loop, port=port, site=site)
       api.start()
       loop.run_forever()
    except KeyboardInterrupt:
        log.error(' Keyboard Interrupt the loop!')
    finally:
        loop.stop()
        loop.close()
