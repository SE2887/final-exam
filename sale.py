import streamlit as st
import pandas as pd
import plotly.express as px

def get_dataframe_from_excel():
	# skiprows=1表示跳过Excel中的第一行，因为第一行是标题
	df = pd.read_excel('D:\\streamlit_env\\supermarket_sales.xlsx',sheet_name='销售数据',skiprows=1,index_col='订单号')

	#pd.to_datatime将'时间'列转换成datetime  
	#format="%H:%M:%S"指定了原有时间字符串的格式
	#.df.hour表示从转换后的数据框取出小时数作为新列
	df['小时数'] = pd.to_datetime(df["时间"],format="%H:%M:%S").dt.hour
	return df


def add_sidebar_func(df):
	with st.sidebar:
		st.header("请筛选数据:")
		city_unique = df["城市"].unique()
		city = st.multiselect("请选择城市:",options=city_unique,default=city_unique)

		customer_type_unique = df["顾客类型"].unique()
		customer_type = st.multiselect("请选择顾客类型:",options=customer_type_unique,default=customer_type_unique)

		gender_unique = df["性别"].unique()
		gender = st.multiselect("请选择性别:",options=gender_unique,default=gender_unique)

		df_selection = df.query("城市 ==@city & 顾客类型 ==@customer_type & 性别 == @gender")

		return df_selection
	

def product_line_chart(df):
	sales_by_product_line = (df.groupby(by=["产品类型"])[["总价"]].sum().sort_values(by="总价"))
	fig_product_sales = px.bar(sales_by_product_line,x="总价",y=sales_by_product_line.index,orientation="h",title="<b>按产品类型划分的销售额<b>")
	return fig_product_sales


def hour_chart(df):
        sales_by_hour = (df.groupby(by=["小时数"])[["总价"]].sum())
        fig_hour_sales = px.bar(sales_by_hour,x=sales_by_hour.index,y="总价",title="<b>按小时数划分的销售额<b>")

        return fig_hour_sales

def main_page_demo(df):
        st.title('📊:销售仪表板')
        left_key_col, middle_key_col, right_key_col = st.columns(3)
        total_sales = int(df["总价"].sum())
        average_rating = round(df["评分"].mean(), 1)
        star_rating_string = ":star:" * int(round(average_rating, 0))
        average_sale_by_transaction = round(df["总价"].mean(), 2)

        with left_key_col:
                st.subheader("总销售额:")
                st.subheader(f"RMB {total_sales:,}")
                
        with middle_key_col:
                st.subheader("顾客评分的平均值:")
                st.subheader(f"{average_rating} {star_rating_string}")

        with right_key_col:
                st.subheader("每单的平均销售额:")
                st.subheader(f"RMB {average_sale_by_transaction}")

        st.divider()

        left_chart_col, right_chart_col = st.columns(2)
        with left_chart_col:
                hour_fig = hour_chart(df)
                st.plotly_chart(hour_fig, use_container_width=True)

        with right_chart_col:
                product_fig = product_line_chart(df)
                st.plotly_chart(product_fig, use_container_width=True)

def run_app():
        st.set_page_config(
                page_title="销售仪表板",
                page_icon=":bar_chart:",
                layout="wide")
        sale_df = get_dataframe_from_excel()
        df_selection = add_sidebar_func(sale_df)
        main_page_demo(df_selection)


if __name__=="__main__":
        run_app()
