import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
from io import BytesIO
import base64


class Graphs:
        
    def get_barplot(df):
        # create a bytes buffer for the image to save
        buffer = BytesIO()
        # create the plot with the use of BytesIO object as its 'file'
        df['date'] = df['date'].astype(str)
        sns.barplot(data=df.groupby('date')['price'].sum().reset_index(), x=df['date'].str.split(n=1, expand=True)[0], y=df['price'])
        plt.xticks(rotation=45, ha='right')
        plt.xlabel('Date')
        plt.ylabel('Total Price')
        plt.title('Total Price per Day')
        plt.savefig(buffer, format='png')
        # set the cursor the begining of the stream
        buffer.seek(0)
        # retreive the entire content of the 'file'
        image_png = buffer.getvalue()
        graph = base64.b64encode(image_png)
        graph = graph.decode('utf-8')
        # free the memory of the buffer
        buffer.close()
        return graph
    
    def get_countplot(df):
        # create a bytes buffer for the image to save
        buffer = BytesIO()
        # create the plot with the use of BytesIO object as its 'file'
        sns.countplot(data=df, x=df['product'])
        plt.xticks(rotation=45, ha='right')
        plt.xlabel('Produit')
        plt.ylabel('Nombre total')
        plt.title('Nombre de ventes par produit')
        plt.savefig(buffer, format='png')
        # set the cursor the begining of the stream
        buffer.seek(0)
        # retreive the entire content of the 'file'
        image_png = buffer.getvalue()
        graph = base64.b64encode(image_png)
        graph = graph.decode('utf-8')
        # free the memory of the buffer
        buffer.close()
        return graph
    
    def get_lineplot(df):
        # create a bytes buffer for the image to save
        buffer = BytesIO()
        # create the plot with the use of BytesIO object as its 'file'
        df['date'] = df['date'].astype(str)
        sns.lineplot(data=df, x=df['date'], y=df['price'])
        plt.xticks(rotation=45, ha='right')
        plt.xlabel('Date')
        plt.ylabel('Total Price')
        plt.title('Total Price per Day')
        plt.savefig(buffer, format='png')
        # set the cursor the begining of the stream
        buffer.seek(0)
        # retreive the entire content of the 'file'
        image_png = buffer.getvalue()
        graph = base64.b64encode(image_png)
        graph = graph.decode('utf-8')
        # free the memory of the buffer
        buffer.close()
        return graph