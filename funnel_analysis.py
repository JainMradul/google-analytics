import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# Define sample data for each column with adjusted action_type categories
data = {
    'visitId': np.random.randint(100000, 999999, size=100),
    'session_date': pd.date_range(start='2023-01-01', periods=100, freq='D'),
    'action_type': np.random.choice(
        ['Click Through of Product Lists', 'Product Detail Views', 'Add to Cart', 
         'Remove from Cart', 'Checkout', 'Completed Purchase'], size=100,p=[.35,.25,.2,.02,.13,.05]),
    'product_name': np.random.choice(['Product A', 'Product B', 'Product C'], size=100),
    'product_price': np.random.uniform(10, 500, size=100).round(2),
    'total_transactions': np.random.randint(0, 10, size=100),
    'total_transaction_revenue': np.random.uniform(0, 2000, size=100).round(2),
    'traffic_medium': np.random.choice(['organic', 'CPC', 'referral'], size=100),
    'device_category': np.random.choice(['desktop', 'mobile', 'tablet'], size=100),
    'user_country': np.random.choice(['USA', 'India', 'Canada', 'Germany'], size=100),
    'traffic_source': np.random.choice(['google', 'direct', 'referral'], size=100),
}

# Create the DataFrame
df = pd.DataFrame(data)

# Display the generated data
print(df.head())


# Define funnel stages
funnel_stages = {
    'Click Through of Product Lists': 'View Product',
    'Product Detail Views': 'Product Detail',
    'Add to Cart': 'Add to Cart',
    'Remove from Cart': 'Remove from Cart',
    'Checkout': 'Checkout',
    'Completed Purchase': 'Purchase'
}

# Sample unique IDs for each visit (for simplicity, using visitId as unique_id)
df['unique_id'] = df['visitId']

# Map action_type to funnel stages
df['funnel_stage'] = df['action_type'].map(funnel_stages)

# Aggregate unique users at each funnel stage
stage_counts = df.groupby('funnel_stage')['unique_id'].nunique().reindex(funnel_stages.values())

# Calculate percentage drop between stages
funnel_percentages = stage_counts / stage_counts.max() * 100

# Funnel chart using Plotly
funnel_data = pd.DataFrame({
    'Stage': stage_counts.index,
    'Users': stage_counts.values,
    'Percentage': funnel_percentages.values
})

fig = px.funnel(funnel_data, x='Users', y='Stage', title='Funnel Analysis')
fig.show()

# Function to get top 3 categories based on unique user counts
def get_top_categories(df, dimension):
    return df.groupby(dimension)['unique_id'].nunique().nlargest(3).index

# Function to visualize funnel by a specific dimension with top 3 categories sequentially
def visualize_top_funnel_by_dimension_sequential(df, dimension):
    top_categories = get_top_categories(df, dimension)
    
    for cat in top_categories:
        stage_counts = df[df[dimension] == cat].groupby('funnel_stage')['unique_id'].nunique().reindex(funnel_stages.values())
        funnel_data = pd.DataFrame({
            'Stage': stage_counts.index,
            'Users': stage_counts.values
        })
        
        fig = go.Figure()
        
        fig.add_trace(
            go.Funnel(
                y=funnel_data['Stage'],
                x=funnel_data['Users'],
                textposition='inside',
                name=cat
            )
        )
        
        fig.update_layout(
            title_text=f'Funnel Analysis for {dimension.capitalize()}: {cat}',
            xaxis_title='Users',
            yaxis_title='Stage'
        )
        
        fig.show()

#Visualize funnel by 'device_category'
visualize_top_funnel_by_dimension_sequential(df, 'traffic_source')