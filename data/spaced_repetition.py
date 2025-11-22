"""Spaced repetition system for intelligent question review."""
from datetime import datetime, timedelta
from typing import Dict, List, Tuple
import json


class SpacedRepetitionSystem:
    """Manages spaced repetition scheduling for questions."""

    def __init__(self):
        self.records: Dict[str, dict] = {}
        self.stats = {
            "total_reviews": 0,
            "total_correct": 0,
            "total_incorrect": 0,
            "streak": 0,
            "best_streak": 0,
        }

    def get_question_record(self, question_id: str) -> dict:
        """Get or create a record for a question."""
        if question_id not in self.records:
            self.records[question_id] = {
                "question_id": question_id,
                "last_seen": None,
                "correct_count": 0,
                "incorrect_count": 0,
                "next_review": datetime.now().isoformat(),
                "interval_days": 0,
                "ease_factor": 2.5,  # Default ease factor (like Anki)
            }
        return self.records[question_id]

    def record_answer(self, question_id: str, is_correct: bool) -> None:
        """Record an answer and update the review schedule."""
        record = self.get_question_record(question_id)
        now = datetime.now()

        # Update counts
        if is_correct:
            record["correct_count"] += 1
            self.stats["total_correct"] += 1
            self.stats["streak"] += 1
            if self.stats["streak"] > self.stats["best_streak"]:
                self.stats["best_streak"] = self.stats["streak"]
        else:
            record["incorrect_count"] += 1
            self.stats["total_incorrect"] += 1
            self.stats["streak"] = 0

        self.stats["total_reviews"] += 1
        record["last_seen"] = now.isoformat()

        # Calculate next review interval using simplified SM-2 algorithm
        if is_correct:
            if record["correct_count"] == 1:
                # First correct answer: review in 1 day
                interval_days = 1
            elif record["correct_count"] == 2:
                # Second correct answer: review in 6 days
                interval_days = 6
            else:
                # Subsequent correct answers: multiply by ease factor
                interval_days = record["interval_days"] * record["ease_factor"]

            # Increase ease factor slightly (max 2.5)
            record["ease_factor"] = min(2.5, record["ease_factor"] + 0.1)
        else:
            # Incorrect answer: review again soon (10 minutes)
            interval_days = 0.007  # ~10 minutes

            # Decrease ease factor (min 1.3)
            record["ease_factor"] = max(1.3, record["ease_factor"] - 0.2)

        record["interval_days"] = interval_days
        record["next_review"] = (now + timedelta(days=interval_days)).isoformat()

    def get_due_questions(self, all_question_ids: List[str], limit: int = 20) -> List[str]:
        """Get questions that are due for review, sorted by urgency."""
        now = datetime.now()

        # Initialize records for any new questions
        for qid in all_question_ids:
            self.get_question_record(qid)

        # Sort questions by next review time (earliest first)
        sorted_questions = sorted(
            all_question_ids,
            key=lambda qid: datetime.fromisoformat(self.records[qid]["next_review"])
        )

        # Return due questions (next_review <= now) plus a few upcoming ones
        due = []
        upcoming = []

        for qid in sorted_questions:
            next_review = datetime.fromisoformat(self.records[qid]["next_review"])
            if next_review <= now:
                due.append(qid)
            elif len(upcoming) < limit // 4:  # Include some upcoming questions
                upcoming.append(qid)

            if len(due) + len(upcoming) >= limit:
                break

        return due + upcoming

    def get_stats(self) -> dict:
        """Get overall statistics."""
        accuracy = 0
        if self.stats["total_reviews"] > 0:
            accuracy = (self.stats["total_correct"] / self.stats["total_reviews"]) * 100

        return {
            **self.stats,
            "accuracy": accuracy,
        }

    def get_topic_stats(self) -> Dict[str, dict]:
        """Get statistics broken down by topic."""
        topic_stats = {}

        for qid, record in self.records.items():
            # Extract topic from question_id (format: "topic_name:index")
            topic = qid.split(":")[0] if ":" in qid else "unknown"

            if topic not in topic_stats:
                topic_stats[topic] = {
                    "correct": 0,
                    "incorrect": 0,
                    "total": 0,
                }

            topic_stats[topic]["correct"] += record["correct_count"]
            topic_stats[topic]["incorrect"] += record["incorrect_count"]
            topic_stats[topic]["total"] += record["correct_count"] + record["incorrect_count"]

        # Calculate accuracy for each topic
        for topic, stats in topic_stats.items():
            if stats["total"] > 0:
                stats["accuracy"] = (stats["correct"] / stats["total"]) * 100
            else:
                stats["accuracy"] = 0

        return topic_stats

    def to_dict(self) -> dict:
        """Export data for storage."""
        return {
            "records": self.records,
            "stats": self.stats,
        }

    def from_dict(self, data: dict) -> None:
        """Import data from storage."""
        if data:
            self.records = data.get("records", {})
            self.stats = data.get("stats", {
                "total_reviews": 0,
                "total_correct": 0,
                "total_incorrect": 0,
                "streak": 0,
                "best_streak": 0,
            })
