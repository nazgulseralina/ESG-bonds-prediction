import requests
import sys

def get_kase_news_from_api(start_date, end_date, output_file):
    base_url = "https://kase.kz/api/news"


    common_params = {
        'per_page': 100,  # Простая пагинация, максимум может быть 100, поэтому поставил 100
        'search': 'bonds',  # это параметр для поиска по слову, можно будет менять если нужно что то еще
        'language': 'en', 
        'start_date': start_date,
        'end_date': end_date,
        'mode': 'normal', # тут желательно не менять 
        'place': 'everywhere', # и тут тоже 
        'rubrics': '3' # Тут рубрикс 3 потому что у тега Instruments на сайте индекс под номером 3
    }
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36'
    }

    page_number = 1
    total_news_found = 0
    all_news = []

    try:
        while True:
            print(f"Fetching page {page_number}...")
            
            current_params = common_params.copy()
            current_params['page'] = page_number 

            response = requests.get(base_url, params=current_params, headers=headers, timeout=15)
            response.raise_for_status()
            
            data = response.json()
            
            news_items = data.get('results', [])

            if not news_items:
                print("No more news items found. Reached the last page.")
                break

            all_news.extend(news_items)
            total_news_found += len(news_items)
            page_number += 1
            
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(f"KASE News (Bonds) from {start_date} to {end_date}\n")
            f.write("=" * 50 + "\n\n")

            if not all_news:
                f.write("No news found for the specified criteria.\n")
            else:
                for item in all_news:
                    title = item.get('subject')
                    date = item.get('create_datetime', 'No Date')
                    link = f"https://kase.kz/en/information/news/show/{item.get('id', '')}/"
                    body = item.get('body', 'No Body')
                    
                    f.write(f"Date: {date[:10]}\n")
                    f.write(f"Title: {title}\n")
                    f.write(f"Link: {link}\n")
                    f.write(f"Body: {body}\n")
                    f.write("-" * 25 + "\n\n")
        
        print(f"\nSuccessfully saved a total of {total_news_found} news items to {output_file}")

    except requests.exceptions.HTTPError as errh:
        print(f"Http Error: {errh}. Check if the API URL or parameters are correct.")
    except requests.exceptions.ConnectionError as errc:
        print(f"Error Connecting: {errc}")
    except requests.exceptions.RequestException as err:
        print(f"An unexpected error occurred: {err}")
    except ValueError:
        print("Error: Could not decode JSON response from API. Response was not valid JSON.")


if __name__ == "__main__":
    
    output_filename = "kase_news.txt"
    
    if len(sys.argv) == 3:
        start_date = sys.argv[1]
        end_date = sys.argv[2]
    else:
        print("No dates provided. Using default range: 2025-09-01 to 2025-10-24")
        start_date = "2024-09-01"
        end_date = "2025-10-24"
        
    get_kase_news_from_api(start_date, end_date, output_filename)