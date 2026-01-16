# Copyright (C) 2026 Talk-Less Contributors
# SPDX-License-Identifier: AGPL-3.0-or-later
#
# This file is part of Talk-Less.
#
# Talk-Less is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Talk-Less is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with Talk-Less. If not, see <https://www.gnu.org/licenses/>.

"""
Database Models for Talk-Less

This module defines SQLAlchemy models for storing summaries and related data.
"""

from sqlalchemy import Column, String, Text, DateTime, Integer, JSON, ForeignKey, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime
import hashlib

Base = declarative_base()


# Association table for many-to-many relationship between summaries and sources
summary_sources = Table(
    'summary_sources',
    Base.metadata,
    Column('summary_id', String(16), ForeignKey('summaries.id')),
    Column('source_article_id', String(16), ForeignKey('source_articles.id'))
)


class Summary(Base):
    """
    Represents a generated news summary.
    """
    __tablename__ = 'summaries'
    
    id = Column(String(16), primary_key=True)
    topic = Column(String(500), nullable=False, index=True)
    summary_text = Column(Text, nullable=False)
    perspectives = Column(JSON, nullable=True)  # List of perspective analyses
    confidence = Column(String(20), default='medium')
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    source_articles = relationship(
        'SourceArticle',
        secondary=summary_sources,
        back_populates='summaries'
    )
    bias_indicators = relationship('BiasIndicatorRecord', back_populates='summary')
    
    def __repr__(self):
        return f"<Summary(id={self.id}, topic={self.topic[:50]})>"
    
    def to_dict(self):
        """Convert to dictionary for API responses."""
        return {
            'id': self.id,
            'topic': self.topic,
            'summary': self.summary_text,
            'perspectives': self.perspectives,
            'confidence': self.confidence,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'source_articles': [article.to_dict() for article in self.source_articles],
            'bias_indicators': [bi.to_dict() for bi in self.bias_indicators],
        }


class SourceArticle(Base):
    """
    Represents a source article used in summaries.
    """
    __tablename__ = 'source_articles'
    
    id = Column(String(16), primary_key=True)
    title = Column(String(1000), nullable=False)
    url = Column(String(2000), nullable=False, unique=True, index=True)
    source_name = Column(String(200), nullable=False, index=True)
    author = Column(String(500), nullable=True)
    published_at = Column(DateTime, nullable=False, index=True)
    fetched_at = Column(DateTime, default=datetime.utcnow)
    content = Column(Text, nullable=True)
    
    # Relationships
    summaries = relationship(
        'Summary',
        secondary=summary_sources,
        back_populates='source_articles'
    )
    
    def __repr__(self):
        return f"<SourceArticle(id={self.id}, title={self.title[:50]})>"
    
    def to_dict(self):
        """Convert to dictionary for API responses."""
        return {
            'id': self.id,
            'title': self.title,
            'url': self.url,
            'source': self.source_name,
            'author': self.author,
            'published_at': self.published_at.isoformat() if self.published_at else None,
        }


class BiasIndicatorRecord(Base):
    """
    Represents a detected bias indicator in a summary or article.
    """
    __tablename__ = 'bias_indicators'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    summary_id = Column(String(16), ForeignKey('summaries.id'), nullable=False)
    indicator_type = Column(String(100), nullable=False, index=True)
    description = Column(Text, nullable=False)
    confidence = Column(String(20), nullable=False)
    examples = Column(JSON, nullable=True)  # List of example strings
    detected_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    summary = relationship('Summary', back_populates='bias_indicators')
    
    def __repr__(self):
        return f"<BiasIndicator(type={self.indicator_type}, confidence={self.confidence})>"
    
    def to_dict(self):
        """Convert to dictionary for API responses."""
        return {
            'type': self.indicator_type,
            'description': self.description,
            'confidence': self.confidence,
            'examples': self.examples,
            'detected_at': self.detected_at.isoformat() if self.detected_at else None,
        }


class PipelineRun(Base):
    """
    Represents a pipeline execution for transparency/audit purposes.
    """
    __tablename__ = 'pipeline_runs'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    started_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)
    status = Column(String(20), nullable=False)  # 'running', 'completed', 'failed'
    articles_fetched = Column(Integer, default=0)
    articles_grouped = Column(Integer, default=0)
    summaries_generated = Column(Integer, default=0)
    bias_indicators_found = Column(Integer, default=0)
    errors = Column(JSON, nullable=True)  # List of error messages
    config_version = Column(String(100), nullable=True)
    
    def __repr__(self):
        return f"<PipelineRun(id={self.id}, status={self.status}, started={self.started_at})>"
    
    def to_dict(self):
        """Convert to dictionary for API responses."""
        return {
            'id': self.id,
            'started_at': self.started_at.isoformat() if self.started_at else None,
            'completed_at': self.completed_at.isoformat() if self.completed_at else None,
            'status': self.status,
            'stats': {
                'articles_fetched': self.articles_fetched,
                'articles_grouped': self.articles_grouped,
                'summaries_generated': self.summaries_generated,
                'bias_indicators_found': self.bias_indicators_found,
            },
            'errors': self.errors,
        }
