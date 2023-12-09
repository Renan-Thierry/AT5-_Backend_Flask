import logging

log = logging
log.basicConfig(level=log.INFO,
                    format='%(asctime)s %(levelname)s %(module)s %(funcName)s %(message)s',
                    handlers=[log.FileHandler("./helpers/logger/app.log", mode='w'),
                              log.StreamHandler()])
stream_handler = [h for h in log.root.handlers if isinstance(
    h, log.StreamHandler)][0]
stream_handler.setLevel(log.INFO)