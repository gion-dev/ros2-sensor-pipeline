#include "rclcpp/rclcpp.hpp"
#include "std_msgs/msg/float64.hpp"
#include <random>
#include <chrono>

class SensorNode : public rclcpp::Node {
public:
    SensorNode() : Node("sensor_node"), gen_(rd_()), dist_(0.0, 1.0), t_(0.0) {

        this->declare_parameter("noise_stddev", 0.5);
        noise_stddev_ = this->get_parameter("noise_stddev").as_double();

        pub_ = this->create_publisher<std_msgs::msg::Float64>("/sensor/raw", 10);

        timer_ = this->create_wall_timer(
            std::chrono::milliseconds(100),
            std::bind(&SensorNode::publish_data, this)
        );

        RCLCPP_INFO(this->get_logger(), "Sensor node started (noise=%.2f)", noise_stddev_);
    }

private:
    void publish_data() {
        t_ += 0.1;

        double signal = sin(t_);
        double noise = dist_(gen_) * noise_stddev_;
        double data = signal + noise;

        std_msgs::msg::Float64 msg;
        msg.data = data;
        pub_->publish(msg);
    }

    std::random_device rd_;
    std::mt19937 gen_;
    std::normal_distribution<> dist_;

    double noise_stddev_;
    double t_;

    rclcpp::Publisher<std_msgs::msg::Float64>::SharedPtr pub_;
    rclcpp::TimerBase::SharedPtr timer_;
};

int main(int argc, char * argv[]) {
    rclcpp::init(argc, argv);
    rclcpp::spin(std::make_shared<SensorNode>());
    rclcpp::shutdown();
    return 0;
}