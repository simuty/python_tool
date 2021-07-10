'''
Author: simuty
Date: 2021-06-07 17:43:59
LastEditTime: 2021-07-03 17:04:40
LastEditors: Please set LastEditors
Description: 
'''
'''
Author: simuty
Date: 2021-06-07 17:26:55
LastEditTime: 2021-06-07 17:43:05
LastEditors: Please set LastEditors
Description:
'''
from utils.log import Logger


log = Logger('test.log',level='debug',when="D")
log.logger.debug('debug')
log.logger.info('info')
log.logger.warning('警告')
log.logger.error('报错')
log.logger.critical('严重')

log.logger.info("Houston, we have a %s", "interesting problem", exc_info=1)
log.logger.info({"ss": 1})

key = "key"
value = "1"

log.logger.info({key: value})



