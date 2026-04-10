#include "rclcpp/rclcpp.hpp"
#include "std_msgs/msg/float64.hpp"

class FilterNode : public rclcpp::Node
{
public:
    FilterNode() : Node("filter_node")
    {
        subscription_ = this->create_subscription<std_msgs::msg::Float64>(
            "/sensor/raw", 10,
            std::bind(&FilterNode::callback, this, std::placeholders::_1));

        publisher_ = this->create_publisher<std_msgs::msg::Float64>("/sensor/filtered", 10);

        RCLCPP_INFO(this->get_logger(), "Filter node started");
    }

private:
    void callback(const std_msgs::msg::Float64::SharedPtr msg)
    {
        double x = msg->data;

        if (!initialized_) {
            prev_y_ = x;
            initialized_ = true;
        }

        double y = alpha_ * x + (1.0 - alpha_) * prev_y_;
        prev_y_ = y;

        auto out_msg = std_msgs::msg::Float64();
        out_msg.data = y;

        publisher_->publish(out_msg);

        RCLCPP_INFO(this->get_logger(), "Filtered: %.3f", y);
    }

    rclcpp::Subscription<std_msgs::msg::Float64>::SharedPtr subscription_;
    rclcpp::Publisher<std_msgs::msg::Float64>::SharedPtr publisher_;

    double alpha_ = 0.2;
    double prev_y_ = 0.0;
    bool initialized_ = false;
};

int main(int argc, char * argv[])
{
    rclcpp::init(argc, argv);
    rclcpp::spin(std::make_shared<FilterNode>());
    rclcpp::shutdown();
    return 0;
}