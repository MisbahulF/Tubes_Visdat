import streamlit as st
import pandas as pd
import plotly.express as px
import time

# Load the dataset
data_path = 'AirbnbData_ready.csv'
data = pd.read_csv(data_path)

# Streamlit app
def main():
    st.set_page_config(page_title="Airbnb Insights Dashboard", layout="wide")

    # Add a narrative structure with sections
    st.title("Airbnb Insights Dashboard: A Data Story")

    st.markdown(
        """### Welcome
        This interactive dashboard explores Airbnb data through engaging visualizations and analyses. Discover insights into pricing trends, geographical distributions, and availability patterns.
        """
    )

    # Sidebar navigation
    st.sidebar.title("Navigation")
    options = ["Introduction", "Explore Dataset", "Price Analysis", "Location Insights", "Reviews & Ratings", "Availability Analysis", "Conclusion"]
    choice = st.sidebar.radio("Go to Section", options)

    if choice == "Introduction":
        st.header("Introduction")
        st.write(
            "This project is designed to provide an interactive exploration of Airbnb data. Use the sidebar to navigate through different sections."
        )

    elif choice == "Explore Dataset":
        st.header("Dataset Overview")
        if st.checkbox("Show Raw Dataset"):
            st.write("Here's the dataset:")
            st.dataframe(data.head())
        
        st.write("### Summary Statistics")
        st.write(data.describe())

    elif choice == "Price Analysis":
        st.header("Price Analysis")
        st.subheader("Price Distribution by Room Type")
        room_filter = st.selectbox("Select Room Type:", options=data['room type'].unique(), index=0)
        filtered_data = data[data['room type'] == room_filter]
        fig1 = px.box(filtered_data, x='room type', y='price', color='room type',
                      title=f"Price Distribution for {room_filter}",
                      labels={'room type': 'Room Type', 'price': 'Price ($)'})
        st.plotly_chart(fig1, use_container_width=True)

        st.subheader("Price Range Across Neighbourhood Groups")
        fig2 = px.violin(data, x='neighbourhood group', y='price', color='neighbourhood group',
                         title="Price Range by Neighbourhood Group",
                         labels={'neighbourhood group': 'Neighbourhood Group', 'price': 'Price ($)'})
        st.plotly_chart(fig2, use_container_width=True)

    elif choice == "Location Insights":
        st.header("Geographical Insights")
        st.subheader("Property Locations by Price")
        price_range = st.slider("Select Price Range:", int(data['price'].min()), int(data['price'].max()), (50, 500))
        map_data = data[(data['price'] >= price_range[0]) & (data['price'] <= price_range[1])]
        fig3 = px.scatter_mapbox(map_data, lat="lat", lon="long", color="price", size="price",
                                 hover_name="NAME", hover_data=["neighbourhood", "price"],
                                 title=f"Map of Properties Priced Between {price_range[0]} and {price_range[1]}",
                                 mapbox_style="open-street-map")
        st.plotly_chart(fig3, use_container_width=True)

        st.subheader("Neighbourhood Distribution")
        neighbourhood_filter = st.multiselect("Select Neighbourhood Groups:", options=data['neighbourhood group'].unique(), default=data['neighbourhood group'].unique())
        neighbourhood_data = data[data['neighbourhood group'].isin(neighbourhood_filter)]
        fig4 = px.histogram(neighbourhood_data, x="neighbourhood", color="neighbourhood group",
                            title="Listings by Selected Neighbourhoods",
                            labels={'neighbourhood': 'Neighbourhood', 'count': 'Number of Listings'})
        st.plotly_chart(fig4, use_container_width=True)

    elif choice == "Reviews & Ratings":
        st.header("Reviews and Ratings Analysis")
        st.subheader("Price vs. Number of Reviews")
        review_range = st.slider("Select Review Count Range:", int(data['number of reviews'].min()), int(data['number of reviews'].max()), (0, 50))
        review_data = data[(data['number of reviews'] >= review_range[0]) & (data['number of reviews'] <= review_range[1])]
        fig5 = px.scatter(review_data, x="number of reviews", y="price", color="neighbourhood group",
                          title=f"Price vs. Number of Reviews (Reviews: {review_range[0]}-{review_range[1]})",
                          labels={'number of reviews': 'Number of Reviews', 'price': 'Price ($)'})
        st.plotly_chart(fig5, use_container_width=True)

        st.subheader("Review Distribution")
        fig6 = px.histogram(data, x="number of reviews", nbins=30, color="neighbourhood group",
                            title="Distribution of Reviews",
                            labels={'number of reviews': 'Number of Reviews', 'count': 'Frequency'})
        st.plotly_chart(fig6, use_container_width=True)

    elif choice == "Availability Analysis":
        st.header("Availability Analysis")
        st.subheader("Availability by Neighbourhood Group")
        fig7 = px.bar(data, x="neighbourhood group", y="availability 365", color="neighbourhood group",
                      title="Availability of Properties by Neighbourhood Group",
                      labels={'neighbourhood group': 'Neighbourhood Group', 'availability 365': 'Availability (Days)'})
        st.plotly_chart(fig7, use_container_width=True)

        st.subheader("Seasonal Availability")
        if "last review" in data.columns:
            data["last_review_month"] = pd.to_datetime(data["last review"], errors='coerce').dt.month
            fig8 = px.histogram(data, x="last_review_month", nbins=12, color="neighbourhood group",
                                title="Seasonal Availability by Last Review Month",
                                labels={'last_review_month': 'Month', 'count': 'Number of Reviews'})
            st.plotly_chart(fig8, use_container_width=True)
        else:
            st.warning("'Last review' data is missing for seasonal analysis.")

    elif choice == "Conclusion":
        st.header("Conclusion")
        st.write(
            """Thank you for exploring this dashboard! We hope these insights provide valuable perspectives on Airbnb listings and their characteristics."""
        )

if __name__ == "__main__":
    main()
