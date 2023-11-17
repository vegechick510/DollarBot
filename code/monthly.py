import helper
import matplotlib
import pandas as pd
import matplotlib.pyplot as plt
matplotlib.use('agg')

def run(message, bot):

    """
    Displays Monthly user expenditure bar chart with and without category wise grouping.
    :return: None (Sends image to bot)
    """
    helper.read_json()
    chat_id = message.chat.id
    user_history = helper.getUserHistory(chat_id)
    if user_history == None:
        bot.send_message(
            chat_id, "Oops! Looks like you do not have any spending records!"
        )
    else:
        try:
            charts = create_chart_for_monthly_analysis(user_history, chat_id)
            for chart in charts:
                with open(chart, "rb") as f:
                    bot.send_photo(chat_id, f)
        except Exception as e:
            print("Exception occurred : " + e)
            bot.reply_to(message, "Oops! Could not create monthly analysis chart")

def create_chart_for_monthly_analysis(user_history, userid):
    result = []

    user_history_split = [item.split(',') for item in user_history]
    df = pd.DataFrame(user_history_split, columns=["Date", "Category", "Cost"])

    # Convert 'Cost' column to numeric
    df['Cost'] = pd.to_numeric(df['Cost'])

    # Convert 'Date' column to datetime
    df['Date'] = pd.to_datetime(df['Date'])

    # Extract month and year from the 'Date' column
    df['Month'] = df['Date'].dt.month_name()
    df['Year'] = df['Date'].dt.year

    # Group by year and month, calculate the total cost for each group
    grouped_data = df.groupby(['Year', 'Month']).agg({'Cost': 'sum'}).reset_index()

    # Plotting the line chart for total expenses
    plt.figure(figsize=(10, 6))
    plt.plot(grouped_data.index, grouped_data['Cost'], marker='o')
    plt.xticks(grouped_data.index, grouped_data['Year'].astype(str) + '-' + grouped_data['Month'])
    plt.xlabel('Year-Month')
    plt.ylabel('Total Cost')
    plt.title('Total Cost Over Time')
    plt.grid(True)
    fig_name = "data/{}_monthly_analysis.png".format(userid)
    plt.savefig(fig_name, bbox_inches="tight")
    result.append(fig_name)

    # Group by year, month, and category, calculate the total cost for each group
    grouped_data = df.groupby(['Year', 'Month', 'Category']).agg({'Cost': 'sum'}).reset_index()

    # Plotting the line chart for each category
    plt.figure(figsize=(12, 6))

    for category in df['Category'].unique():
        category_data = grouped_data[grouped_data['Category'] == category]
        plt.plot(category_data.index, category_data['Cost'], marker='o', label=category)

    plt.xticks(grouped_data.index, grouped_data['Year'].astype(str) + '-' + grouped_data['Month'])
    plt.xlabel('Year-Month')
    plt.ylabel('Total Cost')
    plt.title('Total Cost Over Time by Category')
    plt.legend()
    plt.grid(True)
    fig_name = "data/{}_monthly_analysis_by_category.png".format(userid)
    plt.savefig(fig_name, bbox_inches="tight")
    result.append(fig_name)

    return result