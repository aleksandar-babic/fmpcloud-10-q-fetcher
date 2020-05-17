from Utils import get_logger, setup, safe_get_env_var, unzip_pwd, save_raw_stmnts, merge_excel


def main():
    logger = get_logger()
    setup_res = setup()
    ticker = setup_res['args']['ticker']
    start_range = setup_res['args']['start']
    end_range = setup_res['args']['end']
    logger.info('Base setup successful.')

    api_key = safe_get_env_var('FMPCLOUD_API_KEY')
    logger.info('API key retrieved.')

    zip_path = save_raw_stmnts(setup_res['dirs']['raw'], ticker, api_key)
    extracted_path = unzip_pwd(zip_path)
    logger.info(f'Saved raw financial statements in {extracted_path}.')

    out = merge_excel(extracted_path, setup_res['dirs']['data'], {
        'ticker': ticker,
        'start_date': start_range,
        'end_date': end_range
    })
    logger.info(f"Saved financial statements for {ticker}({out['range']}) in {out['path']}")


if __name__ == '__main__':
    main()
