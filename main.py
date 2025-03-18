import streamlit as st
from scrape import scrape_website, split_dom_content, clean_body_content, extract_body_content
from parse import parse_with_ollama

st.title("AI Web Scraper")

# User input for website URL
url = st.text_input("Enter a website URL:")

if st.button("Scrape site"):
    if url:  # Ensure the URL is not empty
        st.write("Scraping the website...")
        
        result = scrape_website(url)
        if result:
            body_content = extract_body_content(result)
            cleaned_content = clean_body_content(body_content)

            st.session_state.dom_content = cleaned_content  # Store for session persistence

            with st.expander("View More Content"):
                st.text_area("Scraped Content", cleaned_content, height=300)
        else:
            st.error("Failed to scrape the website. It may be blocking bots or using advanced protection.")

    else:
        st.warning("Please enter a valid URL!")


if "dom_content" in st.session_state:
    parse_description=st.text_area("Describe what you want to parse")

    if st.button("Parse Content"):
        if parse_description:
            st.write("Parsing The contet")

            dom_chunks=split_dom_content(st.session_state.dom_content)
            reasult =parse_with_ollama(dom_chunks,parse_description)
            st.write(reasult)
