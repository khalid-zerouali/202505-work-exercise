pipeline_script = new File('/var/jenkins_home/pipeline_script.groovy').getText("UTF-8")
pipelineJob('opensearch-monitors-deployment-pipeline') {
  definition {
    cps {
      script(pipeline_script)
      sandbox(true)
    }
  }
}