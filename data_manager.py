import pandas as pd
import numpy as np

from sentence_transformers import SentenceTransformer
from bertopic import BERTopic


class DataManager:
    def __init__(self, data_path = '.data/'):
        
        self.data_path = data_path
        self.transformer = SentenceTransformer("all-mpnet-base-v2")
        
        self._load_datamodel()
        self._clean_texts()
        
        self.graph_links = None        
        self.umap_embeddings = None
        self.topic_model = None
        self.topics_over_time = None
        
        self.graph = None
        self.author_graph = None
        self.text_graph = None
        
    def _load_datamodel(self):
        
        data_path = self.data_path
        
        meta = pd.read_parquet(data_path + 'model/paragraphs_limited.parquet')
        p_meta = pd.read_parquet(data_path + 'model/paragraphs.parquet')
        self.text_meta = t_meta = pd.read_excel(data_path + 'model/texts.xlsx')
        self.auth_meta = auth_meta = pd.read_excel(data_path + 'model/authors.xlsx')
        
        
        meta = pd.merge(meta, p_meta[['paragraphID', 'textID']], on='paragraphID', how='left')
        meta = pd.merge(meta, t_meta[['textID', 'authorID', 'title', 'date']], on='textID', how='left')
        meta = pd.merge(meta, auth_meta[['authorID', 'name']], on='authorID', how='left')
        
        meta['author_contributions'] = meta.groupby('authorID')['chunkID'].transform('count')
        # meta['text_contributions'] = meta.groupby('textID')['chunkID'].transform('count')
        
        meta.date = pd.to_datetime(meta.date, errors='coerce')
        meta['year'] = meta.date.dt.year
        meta['month'] = meta.date.dt.month
        
        
        self.flat_data = meta
        self.embeddings = np.load(self.data_path + 'model/embeddings.npy')
        

    def _clean_texts(self):
        meta = self.flat_data
        
        filter = ((meta.content.str.match(r'^[\W_]*$')) | (meta.content==''))
        no_cont = meta[filter]
        cont = meta[~filter]
        
        to_rm = no_cont.index.to_list()
        self.embeddings = np.delete(self.embeddings, to_rm, axis=0)
        self.flat_data = cont.reset_index(drop=True)
        
    
    def get_chunk_contents(self, *id):
        meta = self.flat_data
        
        return meta.loc[meta.chunkID.isin(list(id)), 'content'].to_list()
    
    def get_paragraph_contents(self, *id):
        meta = self.flat_data
        
        chunk_ids = meta.loc[meta.paragraphID.isin(list(id)), 'chunkID'].to_list()
        
        return meta.loc[meta.chunkID.isin(chunk_ids), 'content'].to_list()
    
    def get_text_contents(self, *id):
        meta = self.flat_data
        
        out = {i: self.get_paragraph_contents(*meta.loc[meta.textID==i, 'paragraphID'].to_list()) for i in id}
        
        return '\n\n'.join(['\n'.join(v) for k,v in out.items()])
        
        # chunk_ids = meta.loc[meta.textID.isin(list(id)), 'chunkID'].to_list()
        
        # return meta.loc[meta.chunkID.isin(chunk_ids), 'content'].to_list()
        
        
    def _load_topic_model(self):
        
        print('loading topic model...')
        self.topic_model = BERTopic.load(self.data_path + "topic_model/")
        self.topics_over_time = self.topic_model.topics_over_time(self.flat_data.content.values, self.flat_data.date.values, nr_bins=20)
        
        # reconstruct representative docs
        self.topic_model.representative_docs_, _, _, _ = self.topic_model._extract_representative_docs(
            self.topic_model.c_tf_idf_,
            pd.DataFrame({
                'Document': self.flat_data.content,
                'Topic': self.topic_model.topics_
                }),
            self.topic_model.topic_representations_
        )
        
    def _load_umap_embeddings(self):
        self.umap_embeddings = np.load(self.data_path + 'model/umap_embeddings.npy')
        
    def _load_graphs(self):
        self.graph = pd.read_parquet(self.data_path + 'model/graph.parquet')
        self.author_graph = pd.read_parquet(self.data_path + 'model/author_graph.parquet')
        self.text_graph = pd.read_parquet(self.data_path + 'model/text_graph.parquet')
        
        
    def query(self, query_text, show_results = 10):
        embeddings = self.embeddings
        meta = self.flat_data
        query_embedding = self.transformer.encode([query_text])
        distances = np.linalg.norm(embeddings - query_embedding, axis=1)
        closest_indices = np.argsort(distances)[:show_results]
        
        results = meta.iloc[closest_indices].copy()
        results['distance'] = distances[closest_indices]
        
        return results
    

        
        