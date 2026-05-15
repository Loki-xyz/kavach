"""Citation Graph — Network analysis of legal citations

Builds and analyzes citation relationships between cases:
- PageRank for case influence scoring
- Community detection for doctrinal clusters
- Citation chain traversal
- Temporal analysis of legal doctrines
"""

import networkx as nx
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass
from collections import defaultdict
import json

@dataclass
class CaseNode:
    """A case in the citation graph"""
    id: str
    title: str
    citation: str
    court: str
    year: int
    area: str
    importance: str
    pagerank_score: float = 0.0
    citation_count: int = 0
    cited_by_count: int = 0

@dataclass
class CitationEdge:
    """A citation relationship"""
    source: str  # Citing case
    target: str  # Cited case
    relationship: str  # "cites", "distinguishes", "follows", "overrules"
    strength: float = 1.0

class CitationGraph:
    """Graph-based analysis of legal citation networks"""
    
    def __init__(self):
        self.graph = nx.DiGraph()
        self.cases = {}
        
    def add_case(self, case: CaseNode):
        """Add a case node to the graph"""
        self.cases[case.id] = case
        self.graph.add_node(
            case.id,
            title=case.title,
            citation=case.citation,
            court=case.court,
            year=case.year,
            area=case.area,
            importance=case.importance,
        )
    
    def add_citation(self, edge: CitationEdge):
        """Add a citation edge"""
        self.graph.add_edge(
            edge.source,
            edge.target,
            relationship=edge.relationship,
            strength=edge.strength,
        )
    
    def calculate_pagerank(self, damping: float = 0.85) -> Dict[str, float]:
        """Calculate PageRank scores for all cases"""
        if len(self.graph.nodes) == 0:
            return {}
        
        pagerank = nx.pagerank(self.graph, alpha=damping)
        
        # Update case nodes with PageRank scores
        for case_id, score in pagerank.items():
            if case_id in self.cases:
                self.cases[case_id].pagerank_score = score
        
        return pagerank
    
    def get_influential_cases(self, top_k: int = 10) -> List[CaseNode]:
        """Get most influential cases by PageRank"""
        pagerank = self.calculate_pagerank()
        
        sorted_cases = sorted(
            pagerank.items(),
            key=lambda x: x[1],
            reverse=True
        )[:top_k]
        
        return [self.cases[case_id] for case_id, _ in sorted_cases if case_id in self.cases]
    
    def find_citation_chain(self, start_case: str, max_depth: int = 3) -> List[List[str]]:
        """Find citation chains starting from a case"""
        chains = []
        
        def dfs(current: str, path: List[str], depth: int):
            if depth >= max_depth:
                chains.append(path[:])
                return
            
            # Get cases cited by current
            for neighbor in self.graph.successors(current):
                if neighbor not in path:  # Avoid cycles
                    path.append(neighbor)
                    dfs(neighbor, path, depth + 1)
                    path.pop()
            
            # Get cases that cite current
            for neighbor in self.graph.predecessors(current):
                if neighbor not in path:
                    path.append(neighbor)
                    dfs(neighbor, path, depth + 1)
                    path.pop()
            
            if len(path) > 1:
                chains.append(path[:])
        
        dfs(start_case, [start_case], 0)
        
        # Remove duplicates and sort by length
        unique_chains = []
        seen = set()
        for chain in chains:
            chain_key = tuple(chain)
            if chain_key not in seen:
                seen.add(chain_key)
                unique_chains.append(chain)
        
        return sorted(unique_chains, key=len, reverse=True)[:10]
    
    def detect_communities(self) -> Dict[str, List[str]]:
        """Detect communities (doctrinal clusters) in citation network"""
        if len(self.graph.nodes) == 0:
            return {}
        
        # Convert to undirected for community detection
        undirected = self.graph.to_undirected()
        
        # Use Louvain community detection
        try:
            from community import community_louvain
            partition = community_louvain.best_partition(undirected)
        except ImportError:
            # Fallback: connected components
            partition = {}
            for i, component in enumerate(nx.connected_components(undirected)):
                for node in component:
                    partition[node] = i
        
        # Group by community
        communities = defaultdict(list)
        for case_id, community_id in partition.items():
            communities[str(community_id)].append(case_id)
        
        return dict(communities)
    
    def get_citation_influence(self, case_id: str) -> Dict:
        """Get detailed influence metrics for a case"""
        if case_id not in self.graph.nodes:
            return {}
        
        # Calculate various metrics
        in_degree = self.graph.in_degree(case_id)
        out_degree = self.graph.out_degree(case_id)
        
        # PageRank
        pagerank = nx.pagerank(self.graph)
        pr_score = pagerank.get(case_id, 0)
        
        # HITS (hub and authority scores)
        try:
            hubs, authorities = nx.hits(self.graph, max_iter=100)
            hub_score = hubs.get(case_id, 0)
            authority_score = authorities.get(case_id, 0)
        except:
            hub_score = 0
            authority_score = 0
        
        # Betweenness centrality
        betweenness = nx.betweenness_centrality(self.graph)
        betweenness_score = betweenness.get(case_id, 0)
        
        return {
            "case_id": case_id,
            "pagerank": pr_score,
            "hub_score": hub_score,
            "authority_score": authority_score,
            "betweenness_centrality": betweenness_score,
            "cited_by_count": in_degree,
            "cites_count": out_degree,
            "influence_rank": self._get_influence_rank(case_id, pagerank),
        }
    
    def _get_influence_rank(self, case_id: str, pagerank: Dict) -> int:
        """Get the influence rank of a case"""
        sorted_cases = sorted(pagerank.items(), key=lambda x: x[1], reverse=True)
        for rank, (cid, _) in enumerate(sorted_cases, 1):
            if cid == case_id:
                return rank
        return len(sorted_cases) + 1
    
    def find_similar_doctrines(self, case_id: str, top_k: int = 5) -> List[Tuple[str, float]]:
        """Find cases with similar doctrinal focus"""
        if case_id not in self.cases:
            return []
        
        target_case = self.cases[case_id]
        target_area = target_case.area
        
        # Find cases in same area with citation relationships
        similar = []
        for other_id, other_case in self.cases.items():
            if other_id == case_id:
                continue
            
            # Calculate similarity based on area + citation proximity
            area_match = 1.0 if other_case.area == target_area else 0.0
            
            # Citation proximity (shortest path)
            try:
                path_length = nx.shortest_path_length(self.graph, case_id, other_id)
                citation_proximity = 1.0 / (1.0 + path_length)
            except nx.NetworkXNoPath:
                citation_proximity = 0.0
            
            # Combined similarity
            similarity = 0.6 * area_match + 0.4 * citation_proximity
            
            if similarity > 0.3:
                similar.append((other_id, similarity))
        
        return sorted(similar, key=lambda x: x[1], reverse=True)[:top_k]
    
    def get_temporal_evolution(self, area: str) -> List[Dict]:
        """Track how a legal doctrine evolved over time"""
        area_cases = [
            (case.year, case)
            for case in self.cases.values()
            if case.area == area
        ]
        
        area_cases.sort(key=lambda x: x[0])
        
        evolution = []
        for year, case in area_cases:
            influence = self.get_citation_influence(case.id)
            evolution.append({
                "year": year,
                "case_id": case.id,
                "title": case.title,
                "citation": case.citation,
                "pagerank": influence.get("pagerank", 0),
                "cited_by": influence.get("cited_by_count", 0),
            })
        
        return evolution
    
    def export_graph(self) -> Dict:
        """Export graph for visualization"""
        nodes = []
        for case_id, case in self.cases.items():
            nodes.append({
                "id": case_id,
                "label": case.title[:30],
                "citation": case.citation,
                "year": case.year,
                "area": case.area,
                "pagerank": case.pagerank_score,
            })
        
        edges = []
        for source, target, data in self.graph.edges(data=True):
            edges.append({
                "source": source,
                "target": target,
                "relationship": data.get("relationship", "cites"),
            })
        
        return {"nodes": nodes, "edges": edges}
    
    def to_json(self) -> str:
        """Export graph as JSON"""
        return json.dumps(self.export_graph(), indent=2)


def create_indian_citation_graph() -> CitationGraph:
    """Create a pre-populated citation graph for Indian law"""
    graph = CitationGraph()
    
    # Add landmark cases
    cases = [
        CaseNode("vineeta_sharma_2020", "Vineeta Sharma v. Rakesh Sharma", "2020 SCC 9 SC 609", "Supreme Court of India", 2020, "Succession Law", "Landmark"),
        CaseNode("shayara_bano_2017", "Shayara Bano v. Union of India", "2017 SCC 9 SC 1", "Supreme Court of India", 2017, "Constitutional Law", "Landmark"),
        CaseNode("joseph_shine_2018", "Joseph Shine v. Union of India", "2018 SCC 3 SC 1", "Supreme Court of India", 2018, "Criminal Law", "Landmark"),
        CaseNode("puttaswamy_2017", "Justice K.S. Puttaswamy v. Union of India", "2017 SCC 1 SC 1", "Supreme Court of India", 2017, "Constitutional Law", "Landmark"),
        CaseNode("navtej_singh_2018", "Navtej Singh Johar v. Union of India", "2018 SCC 1 SC 1", "Supreme Court of India", 2018, "Constitutional Law", "Landmark"),
        CaseNode("indian_medical_assn_2011", "Indian Medical Association v. Union of India", "2011 SCC 7 SC 1", "Supreme Court of India", 2011, "Consumer Protection", "Landmark"),
        CaseNode("satyawati_sharma_2008", "Satyawati Sharma v. Union of India", "2008 AIR SC 1234", "Supreme Court of India", 2008, "Rent Control", "Important"),
        CaseNode("subhash_kashinath_2019", "Subhash Kashinath Mahajan v. State of Maharashtra", "2019 SCC 6 SC 413", "Supreme Court of India", 2019, "Social Justice", "Important"),
    ]
    
    for case in cases:
        graph.add_case(case)
    
    # Add citation relationships
    citations = [
        CitationEdge("vineeta_sharma_2020", "shayara_bano_2017", "cites"),
        CitationEdge("vineeta_sharma_2020", "joseph_shine_2018", "cites"),
        CitationEdge("navtej_singh_2018", "puttaswamy_2017", "follows"),
        CitationEdge("navtej_singh_2018", "shayara_bano_2017", "cites"),
        CitationEdge("joseph_shine_2018", "puttaswamy_2017", "follows"),
        CitationEdge("subhash_kashinath_2019", "puttaswamy_2017", "distinguishes"),
    ]
    
    for edge in citations:
        graph.add_citation(edge)
    
    return graph
