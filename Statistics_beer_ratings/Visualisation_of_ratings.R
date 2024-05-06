setwd("C:/Users/Robbe Fonteyn/OneDrive - UGent/AJ 2023-2024/Biological Databases/Project/BrewMood/Untappd_ratings.txt")
beer_ratings <- read.table("ratebeer_ratings.txt", header=TRUE, sep="\t")

# Load libraries (assuming you have them installed)
library(ggplot2)

# Sample your data (to avoid memory issues with large files)
data <- head(beer_ratings)  # Adjust sample size as needed

# Create the heatmap
ggplot(beer_ratings, aes(x = username, y = beer_name, fill = taste_rating)) +
  geom_tile(width = 1, height = 1) +  # Adjust width and height for better resolution
  scale_fill_distiller(palette = "Blues") +  # Choose your desired color palette
  labs(title = "Taste Ratings", x = "Username", y = "beer_name") +
  theme_minimal()

ggplot(beer_ratings, aes(x = beer_name, y = taste_rating)) +
  geom_boxplot() +
  labs(title = "Distribution of Taste Ratings for Different Beers",
       x = "Beer Name", y = "Taste Rating")

ggplot(beer_ratings, aes(x = beer_name, y = taste_rating, fill = beer_name)) +
  geom_violin() +
  labs(title = "Distribution of Taste Ratings for Different Beers",
       x = "Beer Name", y = "Taste Rating")

# Assuming beer_ratings is your data frame
ggplot(beer_ratings, aes(x = beer_name, fill = factor(taste_rating))) +
  geom_bar() +
  labs(title = "Distribution of Taste Ratings for Different Beers",
       x = "Beer Name", y = "Count of Ratings",
       fill = "Taste Rating")

### Filter out low rated beers ####
# Assuming your data frame is named beer_ratings

library(dplyr)
library(ggplot2)

# Step 1: Calculate count of ratings for each beer
beer_counts <- beer_ratings %>%
  group_by(beer_name) %>%
  summarise(count_ratings = n())

# Step 2: Filter out beers with fewer than 50 ratings
popular_beers <- beer_counts %>%
  filter(count_ratings >= 50) %>%
  arrange(desc(count_ratings)) %>% # Arrange in descending order of count_ratings
  pull(beer_name) # Get the names of popular beers as a vector


# Step 3: Filter the original data for popular beers and create the visualization
popular_beer_ratings <- beer_ratings %>%
  filter(beer_name %in% popular_beers)

# Step 4: Reorder the beer names based on the count of ratings
popular_beer_ratings$beer_name <- factor(popular_beer_ratings$beer_name, levels = popular_beers)

# Now you can create the visualization using popular_beer_ratings
# For example, let's create a bar plot
ggplot(popular_beer_ratings, aes(x = beer_name, fill = factor(taste_rating))) +
  geom_bar() +
  geom_text(aes=label()) +
  labs(title = "Distribution of Taste Ratings for Popular Beers (>=50 ratings)",
       x = "Beer Name", y = "Count of Ratings",
       fill = "Taste Rating") +
  theme(axis.text.x = element_text(angle = 90, vjust = 0.5, hjust=1))


####### Get beers that are rated 8/ higher on average #########
# Calculate average rating for each beer
beer_avg_ratings <- beer_ratings %>%
  group_by(beer_name) %>%
  summarize(avg_rating = mean(taste_rating),
            num_ratings = n()) %>%
  filter(avg_rating >= 8) %>%
  arrange(desc(num_ratings))

# Plot the results
ggplot(beer_avg_ratings, aes(x = reorder(beer_name, num_ratings), y = num_ratings)) +
  geom_bar(stat = "identity", fill = "skyblue") +
  labs(title = "Beers with Average Rating of 8 or Higher",
       x = "Beer Name",
       y = "Number of Ratings") +
  theme(axis.text.x = element_text(angle = 45, hjust = 1)) +
  coord_flip()

############################ Another visualization ####################
# Step 1: Calculate count of ratings and average rating for each beer
beer_summary <- beer_ratings %>%
  group_by(beer_name) %>%
  summarise(count_ratings = n(),
            average_rating = mean(taste_rating))

# Step 2: Filter out beers with fewer than 10 ratings
popular_beers <- beer_summary %>%
  filter(count_ratings >= 50) %>%
  arrange(desc(count_ratings)) %>%
  pull(beer_name) # Get the names of popular beers as a vector

# Step 3: Filter the original data for popular beers and create the visualization
popular_beer_data <- beer_ratings %>%
  filter(beer_name %in% popular_beers)

# Step 4: Reorder the beer names based on the count of ratings
popular_beer_data$beer_name <- factor(popular_beer_data$beer_name, levels = popular_beers)

# Now you can create the visualization using popular_beer_data
# For example, let's create a bar plot with average rating labels
ggplot(popular_beer_data, aes(x = beer_name,)) +
  geom_bar() +
  geom_text(data = beer_summary, aes(label = round(average_rating, 1), y = average_rating + 0.1), 
            position = position_dodge(width = 0.9), vjust = -0.5, size = 3, color = "black") +
  labs(title = "Distribution of Taste Ratings for Popular Beers (>=10 ratings)",
       x = "Beer Name", y = "Count of Ratings",
       fill = "Taste Rating") +
  theme(axis.text.x = element_text(angle = 90, vjust = 0.5, hjust=1))
