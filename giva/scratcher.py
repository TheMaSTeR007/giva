import json

import unicodedata

s = r'''{
      "@context": "http://schema.org/",
      "@type": "Product",
      "name": "Silver Drizzle Drop Pendant with Box Chain",
      "url": "https:\/\/www.giva.co\/products\/silver-drizzle-drop-pendant-with-box-chain",
      "image": [
          "https:\/\/www.giva.co\/cdn\/shop\/files\/PD0179_1.jpg?v=1711632098\u0026width=1920"
        ],
      "description": "\n\nThe Inspiration:Let this beautiful pendant drizzle its charm over your evening. Isn't it the perfect complement to your dinner date outfit?The Design:This silver pendant features a circular motif with zircons, with a large zircon placed at its centre.\n\n925 Silver \nPerfect for sensitive skin\nLength of chain: 45 cm + 4 cm Adjustable\n\nMotif Height: 2.1 cm, Width: 1.1 cm \n\nComes with the GIVA Jewellery kit and authenticity certificate\nContent: Set\n\nNet Qty- 1 unit\n\nStyling Tip:Team this with a shirt dress.\n",
      "sku": "PD0179",
      "brand": {
        "@type": "Brand",
        "name": "GIVA Jewellery"
      },
      "offers": [{
            "@type" : "Offer","sku": "PD0179","availability" : "http://schema.org/InStock",
            "price" : 1999.0,
            "priceCurrency" : "INR",
            "url" : "https:\/\/www.giva.co\/products\/silver-drizzle-drop-pendant-with-box-chain?variant=36828242116770"
          }
]
      
      ,"aggregateRating": {
          "@type": "AggregateRating",
          "ratingValue": 5.0,
          "reviewCount": 100
        }
      
    }'''
json_text = json.loads(s.replace('\n', '').replace(r'\/', '/'))
print(type(json_text))
for js in json_text:
    print(js)
    print(json_text[js])
    print('-'*100)
