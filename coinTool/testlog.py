'''
Author: simuty
Date: 2021-06-07 17:43:59
<<<<<<< HEAD
LastEditTime: 2021-06-10 18:36:27
=======
LastEditTime: 2021-06-19 17:08:25
>>>>>>> ea51fae3b7de1376f29a01461117180c72e6aa71
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



