import streamlit as st
import requests
from bs4 import BeautifulSoup as bs
from urllib.request import urlopen as uReq

def main():
    st.title("This is a Flipkart review web scrapper!!")
    st.subheader("You can search any object's review with this tool.")
    x = st.text_input("Enter the Search String")
    if st.button("Search"):
        search_string = x.replace(" ", "")
        flipkart_url = "https://www.flipkart.com/search?q=" + search_string
        uClient = uReq(flipkart_url)
        flipkart_page = uClient.read()
        uClient.close()
        flipkart_html = bs(flipkart_page, "html.parser")
        big_boxes = flipkart_html.find_all("div", {"class:", "_1AtVbE col-12-12"})
        del big_boxes[0:3]
        box = big_boxes[0]
        product_link = "https://flipkart.com" + box.div.div.div.a['href']
        prod_res = requests.get(product_link)
        prod_res.encoding = 'utf-8'
        prod_html = bs(prod_res.text, "html.parser")
        print(prod_html)
        comment_boxes = prod_html.find_all('div', {'class': "_16PBlm"})

        filename = search_string + '.csv'
        fw = open(filename, "w")
        headers = "Products, Customer Name, Rating, Heading, Comment \n"
        fw.write(headers)
        reviews = []

        for comment_box in comment_boxes:
            try:
                name = comment_box.div.div.find_all('p', {'class': '_2sc7ZR _2V5EHH'})[0].text
            except:
                name = "No name"

            try:
                rating = comment_box.div.div.div.div.text

            except:
                rating = "No Rating"

            try:
                # commentHead.encode(encoding='utf-8')
                commentHead = comment_box.div.div.div.p.text

            except:
                commentHead = 'No Comment Heading'
            try:
                comtag = comment_box.div.div.find_all('div', {'class': ''})
                # custComment.encode(encoding='utf-8')
                custComment = comtag[0].div.text
            except Exception as e:
                print("Exception while creating dictionary: ", e)

            mydict = {"Product": search_string, "Name": name, "Rating": rating, "CommentHead": commentHead,
                      "Comment": custComment}
            reviews.append(mydict)

        reviews = reviews[0:(len(reviews) - 1)]
        st.dataframe(reviews)


if __name__ == '__main__':
    main()
