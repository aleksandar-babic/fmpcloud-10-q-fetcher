from Utils import get_logger, setup, safe_get_env_var, rm_dir, process_tickers, get_tickers


def main():
    logger = get_logger()
    setup_res = setup()
    logger.info('Base setup successful.')

    api_key = safe_get_env_var('FMPCLOUD_API_KEY')
    logger.info('API key retrieved.')

    tickers_config = {
        'api_key': api_key,
        'dirs': setup_res['dirs'],
        'tickers': get_tickers(setup_res['args']),
    }
    try:
        process_tickers(tickers_config, logger)
    finally:
        try:
            rm_dir(setup_res['dirs']['raw'])
            logger.debug('Deleted raw financial statements.')
        except FileNotFoundError:
            logger.debug('Nothing to cleanup.')


if __name__ == '__main__':
    main()
