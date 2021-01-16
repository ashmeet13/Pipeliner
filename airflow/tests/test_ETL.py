import unittest

from airflow.models import DagBag


class TestETL(unittest.TestCase):
    def setUp(self):
        self.dagbag = DagBag()
        self.dag_id = "simple_etl"

    def test_task_count(self):
        dag = self.dagbag.get_dag(self.dag_id)
        self.assertEqual(len(dag.tasks), 3)

    def test_contain_tasks(self):
        dag = self.dagbag.get_dag(self.dag_id)
        tasks = dag.tasks
        task_ids = list(map(lambda task: task.task_id, tasks))
        self.assertCountEqual(
            task_ids,
            ["extract_total_sales", "extract_brand_wise_sales", "send_slack_message"],
        )

    def test_dependencies_of_extract_total_sales(self):
        dag = self.dagbag.get_dag(self.dag_id)
        fetched_task = dag.get_task("extract_total_sales")

        upstream_task_ids = list(
            map(lambda task: task.task_id, fetched_task.upstream_list)
        )
        self.assertCountEqual(upstream_task_ids, [])
        downstream_task_ids = list(
            map(lambda task: task.task_id, fetched_task.downstream_list)
        )
        self.assertCountEqual(downstream_task_ids, ["send_slack_message"])

    def test_dependencies_of_extract_brand_wise_sales(self):
        dag = self.dagbag.get_dag(self.dag_id)
        fetched_task = dag.get_task("extract_brand_wise_sales")

        upstream_task_ids = list(
            map(lambda task: task.task_id, fetched_task.upstream_list)
        )
        self.assertCountEqual(upstream_task_ids, [])
        downstream_task_ids = list(
            map(lambda task: task.task_id, fetched_task.downstream_list)
        )
        self.assertCountEqual(downstream_task_ids, ["send_slack_message"])

    def test_dependencies_of_send_slack_message(self):
        dag = self.dagbag.get_dag(self.dag_id)
        fetched_task = dag.get_task("send_slack_message")

        upstream_task_ids = list(
            map(lambda task: task.task_id, fetched_task.upstream_list)
        )
        self.assertCountEqual(
            upstream_task_ids, ["extract_brand_wise_sales", "extract_total_sales"]
        )
        downstream_task_ids = list(
            map(lambda task: task.task_id, fetched_task.downstream_list)
        )
        self.assertCountEqual(downstream_task_ids, [])


suite = unittest.TestLoader().loadTestsFromTestCase(TestETL)
unittest.TextTestRunner(verbosity=2).run(suite)
