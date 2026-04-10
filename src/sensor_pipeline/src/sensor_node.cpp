#include "rclcpp/rclcpp.hpp"
#include "std_msgs/msg/float64.hpp"
#include <chrono>
#include <random>

using namespace std::chrono_literals;

class SensorNode : public rclcpp::Node
{
public:
    SensorNode() : Node("sensor_node"), dist_(0.0, 1.0)
    {
        publisher_ = this->create_publisher<std_msgs::msg::Float64>("/sensor/raw", 10);

        timer_ = this->create_wall_timer(
            100ms, std::bind(&SensorNode::publish_data, this));

        RCLCPP_INFO(this->get_logger(), "Sensor node started");
    }

private:
    void publish_data()
    {
        auto message = std_msgs::msg::Float64();

        double noise = dist_(mt_);
        double value = std::sin(time_) + noise * 0.2;

        message.data = value;

        publisher_->publish(message);

        RCLCPP_INFO(this->get_logger(), "Raw: %.3f", value);

        time_ += 0.1;
    }

    rclcpp::Publisher<std_msgs::msg::Float64>::SharedPtr publisher_;
    rclcpp::TimerBase::SharedPtr timer_;

    std::mt19937 mt_{std::random_device{}()};
    std::normal_distribution<double> dist_;

    double time_ = 0.0;
};

int main(int argc, char * argv[])
{
    rclcpp::init(argc, argv);
    rclcpp::spin(std::make_shared<SensorNode>());
    rclcpp::shutdown();
    return 0;
}