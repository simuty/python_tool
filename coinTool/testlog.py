'''
Author: simuty
Date: 2021-06-07 17:43:59
LastEditTime: 2021-06-19 17:08:25
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


log = Logger('./all.log',level='debug')
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



