import matplotlib.pyplot as plt
import streamlit as st
import seaborn as sns
import base64


def render_image(filepath: str):
    """
   filepath: path to the image. Must have a valid file extension.
   """
    mime_type = filepath.split('.')[-1:][0].lower()
    with open(filepath, "rb") as f:
        content_bytes = f.read()
    content_b64encoded = base64.b64encode(content_bytes).decode()
    image_string = f'data:image/{mime_type};base64,{content_b64encoded}'
    st.image(image_string)


# Disclaimer text
disclaimer = """
Welcome to my database project called Brewify!

Please read the following disclaimer before using this website:   
**Age Verification**:  
You must be of legal drinking age in your country to use this application. By accessing and
using this website, you are confirming that you are of legal drinking age.

**Educational Purposes**:  
Please note that Brewify is intended for educational purposes only. The information
provided on this application is for educational and informational purposes regarding alcoholic beverages. It is not
intended to promote excessive alcohol consumption or any irresponsible behavior related to alcohol.

**Drink Responsibly**:  
Please drink responsibly. Alcohol should be consumed in moderation, and excessive
consumption can be harmful to health. If you choose to drink alcoholic beverages, please do so responsibly and in
accordance with the laws and regulations of your country.

**Accuracy of Information**:  
While I strive to provide accurate and up-to-date information, I cannot guarantee the
accuracy or completeness of the information provided. The content on this website is for general informational
purposes only. Please verify any information with the appropriate sources before making decisions based on it.

**Acceptance of Terms**:  
By using this website, you accept and agree to the terms and conditions outlined in this disclaimer.
If you do not agree with any part of this disclaimer, please refrain from using this application."""


# Function to fetch data from MySQL database
def fetch_data(query):
    # Connect to MySQL database
    conn = st.connection('mysql', type="sql")
    try:
        df = conn.query(query)
        return df
    except Exception as e:
        st.error(f"An error occurred: {e}\n with the query: {query}")


# Function to fetch distinct beer styles from the database
def get_beer_styles():
    query = "SELECT DISTINCT style_name FROM styles"
    styles_df = fetch_data(query)
    return styles_df['style_name'].tolist()


# Function to fetch distinct location names from the database
def get_location_names():
    query = "SELECT DISTINCT location_name FROM beers"
    locations_df = fetch_data(query)
    return locations_df['location_name'].tolist()


def get_production_status():
    query = "Select Distinct production_status From beers"
    production_df = fetch_data(query)
    return production_df['production_status'].tolist()


# Main function to run the Streamlit app
def main():
    st.set_page_config(page_title="Brewify", layout="wide", page_icon=":beer:")

    # Title of the app
    st.title(
        "Brewify - Find the Perfect Belgian Beer! :flag-be::beer:")

    # Display disclaimer
    accepted = st.checkbox("I accept the terms and conditions", key="accept_checkbox")
    if not accepted:
        st.markdown(disclaimer)
        return

    # Sidebar things
    sidb = st.sidebar
    sidb.title("Customize your search:")
    advance_search = sidb.toggle('Advance Search')

    if advance_search:
        st.sidebar.subheader("Advanced Beer Search")
        beer_name = st.sidebar.text_input("Filter by Beer Name", "")
        abv_range = st.sidebar.slider("Filter by ABV (Alchohol By Volume) Range", 0.0, 20.0, (0.0, 20.0), 0.1)
        ibu_range = st.sidebar.slider("Filter by IBU (International Bitterness Units) Range", 0, 100, (0, 100), 1)
        beer_styles = get_beer_styles()
        selected_style = st.sidebar.selectbox("Filter by Beer Style", [""] + beer_styles)
        brewery_name = st.sidebar.text_input("Filter by Brewery Name", "")
        min_rating = st.sidebar.slider("Filter by Minimum Rating", 0.0, 5.0, 0.0, 0.1)
        locations = get_location_names()
        selected_location = st.sidebar.selectbox("Filter by Location", [""] + locations)
        production_status = get_production_status()
        production_status = st.sidebar.selectbox("Filter by Production Status", [""] + production_status)
        include_null_values = st.sidebar.toggle("Include None values", True)
        show_plot = st.sidebar.toggle("Show Plots", False)

        query_conditions = []

        if beer_name:
            query_conditions.append(f"beers.beer_name LIKE '%{beer_name}%'")
        if brewery_name:
            query_conditions.append(f"breweries.brewery_name LIKE '%{brewery_name}%'")
        if min_rating:
            query_conditions.append(f"ratings.rating >= {min_rating}")
        if selected_style:
            query_conditions.append(f"styles.style_name = '{selected_style}'")
        if selected_location:
            query_conditions.append(f"beers.location_name = '{selected_location}'")
        if abv_range:
            min_abv, max_abv = abv_range
            abv_condition = f"(beers.abv IS NULL OR (beers.abv >= {min_abv} AND beers.abv <= {max_abv}))"
            if not include_null_values:
                abv_condition = f"beers.abv >= {min_abv} AND beers.abv <= {max_abv}"
            query_conditions.append(abv_condition)
        if ibu_range:
            min_ibu, max_ibu = ibu_range
            ibu_condition = f"(beers.ibu IS NULL OR (beers.ibu >= {min_ibu} AND beers.ibu <= {max_ibu}))"
            if not include_null_values:
                ibu_condition = f"beers.ibu >= {min_ibu} AND beers.ibu <= {max_ibu}"
            query_conditions.append(ibu_condition)
        if production_status:
            query_conditions.append(f"beers.production_status = '{production_status}'")

        query = """            SELECT beers.beer_name AS 'Beer Name',
                   beers.abv AS 'ABV (%)',
                   beers.ibu AS 'IBU',
                   styles.style_name AS 'Style',
                   breweries.brewery_name AS 'Brewery',
                   ratings.rating AS 'Rating (on 5)',
                   beers.location_name AS 'Location',
                   beers.production_status AS 'Production Status'
        FROM beers JOIN breweries ON beers.brewery_id = 
        breweries.brewery_id JOIN ratings ON beers.rating_id = ratings.rating_id JOIN styles ON beers.style_id = 
        styles.style_id"""
        if query_conditions:
            query += " WHERE " + " AND ".join(query_conditions)

        results = fetch_data(query)

        if results is not None and not results.empty:
            st.write(results)
            st.write("Total results found:", len(results))

            if show_plot:
                st.title("Plots based on the current results:")
                st.markdown("""
                The plot illustrates the distribution of beers across different styles in the dataset. 
                Y-axis shows the beer styles, while the X-axis shows to the count of 
                beers belonging to that particular style. In case of a large number of styles, the plot becomes
                difficult to interpret and read.""")
                # Plot number of beers per style
                style_counts = results['Style'].value_counts()
                plt.figure(figsize=(10, 6))
                style_counts.plot(kind='barh')
                plt.title("Number of Beers per Style")
                plt.xlabel("Count")
                plt.ylabel("Beer Style")
                st.pyplot(plt)

                st.write('')
                st.markdown("""
                This plot shows the distribution of ABV (Alcohol By Volume) values for the beers in the result.
                """)
                # Histogram of ABV
                plt.figure(figsize=(10, 6))
                sns.histplot(results['ABV (%)'].dropna(), bins=20, kde=True)
                plt.title("Distribution of ABV")
                plt.xlabel("ABV (%)")
                plt.ylabel("Frequency")
                st.pyplot(plt)

                st.write("")
                st.markdown("""
                The plot below shows the distribution of IBU (International Bitterness Units) values for the beers in the result.
                """)
                # Histogram of IBU
                plt.figure(figsize=(10, 6))
                sns.histplot(results['IBU'].dropna(), bins=20, kde=True)
                plt.title("Distribution of IBU")
                plt.xlabel("IBU")
                plt.ylabel("Frequency")
                st.pyplot(plt)

                st.write("")
                st.markdown("""
                The box plot below shows the distribution of ABV values for different beer styles. This plot can become
                uninterpretable if there are too many styles in the search result.
                """)
                plt.figure(figsize=(10, 6))
                sns.boxplot(data=results, y='Style', x='ABV (%)', orient='h')
                plt.title("Distribution of ABV by Beer Style")
                plt.xlabel("ABV (%)")
                plt.ylabel("Beer Style")
                plt.yticks(rotation=0)
                st.pyplot(plt)

                st.write("")
                st.markdown("""
                A Scatter plot of ABV vs IBU values for the beers in the result. The plot shows the relationship
                between the Alcohol By Volume (ABV) and International Bitterness Units (IBU) of the beers in the results.
                """)
                # Scatter plot of ABV vs IBU
                plt.figure(figsize=(10, 6))
                sns.scatterplot(data=results, x='ABV (%)', y='IBU')
                plt.title("ABV vs IBU")
                plt.xlabel("ABV (%)")
                plt.ylabel("IBU")
                st.pyplot(plt)

                st.write("")
                st.markdown("""
                The pie chart below shows the distribution of beer styles in the result.
                """)
                # Pie chart of Beer Styles
                style_counts = results['Style'].value_counts()
                other_styles = style_counts[style_counts / style_counts.sum() < 0.02]
                style_counts = style_counts[style_counts / style_counts.sum() >= 0.02]
                if not other_styles.empty:
                    other_styles_count = other_styles.sum()
                    style_counts['Other'] = other_styles_count

                plt.figure(figsize=(10, 6))
                plt.pie(style_counts, labels=style_counts.index, autopct='%1.1f%%', startangle=140)
                plt.title("Distribution of Beer Styles")
                st.pyplot(plt)

        else:
            st.write("No results found.")

    else:
        st.sidebar.subheader("Default Search")
        beer_name = st.sidebar.text_input("Filter by Beer Name", "")

        if beer_name == "jembe" or beer_name == "jembeken" or beer_name == "jemme":
            render_image("Jomb.jpg")
            render_image("Jomb2.jpg")

        if beer_name == "raggie":
            render_image("Rag4.jpg")
            render_image("rag_lor.jpg")
            render_image("Rag2.jpg")
            render_image("Rag3.jpg")

        if beer_name == "dekkie" or beer_name == "sokkie" or beer_name == "sekkiesekkie":
            render_image("sokkie.png")
            render_image("Sokiewokie.jpg")

        # Query to fetch data from MySQL database
        query = f"""             SELECT beers.beer_name AS 'Beer Name',
                   beers.abv AS 'ABV (%)',
                   beers.ibu AS 'IBU',
                   styles.style_name AS 'Style',
                   breweries.brewery_name AS 'Brewery',
                   ratings.rating AS 'Rating (on 5)',
                   beers.location_name AS 'Location',
                   beers.production_status AS 'Production Status'
        FROM beers JOIN breweries ON beers.brewery_id = 
        breweries.brewery_id JOIN ratings ON beers.rating_id = ratings.rating_id JOIN styles ON beers.style_id = 
        styles.style_id WHERE beers.beer_name LIKE '%{beer_name}%'
        """

        results = fetch_data(query)

        if results is not None and not results.empty:
            st.write(results)
            st.write("Total results found:", len(results))
        else:
            st.write("No results found.")


if __name__ == "__main__":
    main()
